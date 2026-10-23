import json
import uuid
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
import aiosqlite

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=4, max_length=128)
    phone: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    district: Optional[str] = None
    profile_data: Optional[Dict[str, Any]] = None

class LoginRequest(BaseModel):
    identifier: str = Field(..., description="Name, phone number, or email")
    password: str = Field(..., min_length=1)

class UpdateProfileRequest(BaseModel):
    profile_data: Dict[str, Any]

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest):
    """Registers a new citizen account with encrypted credentials and profile."""
    name_clean = req.name.strip()
    phone_clean = req.phone.strip() if req.phone else None
    email_clean = req.email.strip().lower() if req.email else None

    # Merge top-level demographic fields into profile_data
    profile = dict(req.profile_data or {})
    profile.setdefault("name", name_clean)
    if phone_clean:
        profile.setdefault("phone", phone_clean)
    if req.age is not None:
        profile["age"] = req.age
    if req.gender:
        profile["gender"] = req.gender
    if req.district:
        profile["district"] = req.district

    password_hash, salt = hash_password(req.password)
    user_id = str(uuid.uuid4())

    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row

        # Check if citizen with same phone exists (if phone provided)
        if phone_clean:
            cursor = await db.execute("SELECT id FROM users WHERE phone = ?", (phone_clean,))
            if await cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A citizen account with this mobile number already exists."
                )

        # Check if exact name exists to avoid ambiguity if phone isn't provided
        cursor = await db.execute("SELECT id FROM users WHERE LOWER(name) = LOWER(?)", (name_clean,))
        existing_user = await cursor.fetchone()
        if existing_user and not phone_clean:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This citizen name is already registered. Please provide a mobile number or choose a unique name."
            )

        # Insert new user
        await db.execute("""
            INSERT INTO users (id, name, phone, email, password_hash, salt, profile_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            name_clean,
            phone_clean,
            email_clean,
            password_hash,
            salt,
            json.dumps(profile, ensure_ascii=False)
        ))
        await db.commit()

    token = create_access_token(user_id=user_id, name=name_clean, extra_data={"phone": phone_clean})

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user={
            "id": user_id,
            "name": name_clean,
            "phone": phone_clean,
            "profile": profile
        }
    )

@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    """Authenticates a citizen with their password and returns a secure JWT."""
    ident = req.identifier.strip()

    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # Search by phone, email, or name
        cursor = await db.execute("""
            SELECT id, name, phone, email, password_hash, salt, profile_data
            FROM users
            WHERE phone = ? OR LOWER(email) = LOWER(?) OR LOWER(name) = LOWER(?)
            ORDER BY created_at DESC
            LIMIT 1
        """, (ident, ident, ident))
        
        user_row = await cursor.fetchone()
        if not user_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials. Citizen account not found.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password hash
        is_valid = verify_password(req.password, user_row["password_hash"], user_row["salt"])
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password. Please check and try again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        profile = {}
        if user_row["profile_data"]:
            try:
                profile = json.loads(user_row["profile_data"])
            except Exception:
                profile = {}

    token = create_access_token(user_id=user_row["id"], name=user_row["name"], extra_data={"phone": user_row["phone"]})

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user={
            "id": user_row["id"],
            "name": user_row["name"],
            "phone": user_row["phone"],
            "profile": profile
        }
    )

@router.get("/me")
async def get_current_citizen(user_payload: Dict[str, Any] = Depends(get_current_user)):
    """Returns the authenticated citizen profile from secure database."""
    user_id = user_payload.get("sub")
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT id, name, phone, email, profile_data, created_at
            FROM users
            WHERE id = ?
        """, (user_id,))
        user_row = await cursor.fetchone()
        if not user_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Citizen account not found."
            )

        profile = {}
        if user_row["profile_data"]:
            try:
                profile = json.loads(user_row["profile_data"])
            except Exception:
                profile = {}

        return {
            "id": user_row["id"],
            "name": user_row["name"],
            "phone": user_row["phone"],
            "profile": profile
        }

@router.put("/profile")
async def update_citizen_profile(
    req: UpdateProfileRequest,
    user_payload: Dict[str, Any] = Depends(get_current_user)
):
    """Updates the citizen profile for the authenticated account."""
    user_id = user_payload.get("sub")
    profile_json = json.dumps(req.profile_data, ensure_ascii=False)

    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute("""
            UPDATE users
            SET profile_data = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (profile_json, user_id))
        await db.commit()

    return {"status": "ok", "message": "Profile updated successfully", "profile": req.profile_data}
