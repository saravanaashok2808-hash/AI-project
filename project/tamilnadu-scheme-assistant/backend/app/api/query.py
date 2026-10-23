import json
import logging
import re
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import httpx
import aiosqlite

from app.models.query import QueryRequest, QueryResponse
from app.services.assistant_service import assistant_service
from app.ai.llm.gemini_service import gemini_service
from app.core.security import get_current_user_optional
from app.core.config import settings, BASE_DIR

logger = logging.getLogger(__name__)
router = APIRouter()

def save_key_to_env(key: str):
    """Saves the active Gemini API key to settings and .env so it permanently persists."""
    try:
        cleaned = key.strip()
        settings.GEMINI_API_KEY = cleaned
        env_path = BASE_DIR / ".env"
        if env_path.exists():
            content = env_path.read_text(encoding="utf-8")
            if "GEMINI_API_KEY=" in content:
                content = re.sub(r"GEMINI_API_KEY=.*", f"GEMINI_API_KEY={cleaned}", content)
            else:
                content += f"\nGEMINI_API_KEY={cleaned}\n"
            env_path.write_text(content, encoding="utf-8")
            logger.info("Successfully persisted Gemini API key to .env file.")
    except Exception as e:
        logger.warning(f"Could not persist key to .env: {e}")

class GeminiValidateRequest(BaseModel):
    api_key: str

@router.post("/validate-gemini")
async def validate_gemini_key(req: GeminiValidateRequest):
    key = req.api_key.strip()
    if not key:
        return {"valid": False, "error": "API key cannot be empty"}
    
    # Auto-discover the exact model supported by this key
    best_model = await gemini_service.discover_best_model(key)
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "Hello"}]}],
        "generationConfig": {"maxOutputTokens": 5}
    }
    
    for ver in ["v1beta", "v1"]:
        endpoint = f"https://generativelanguage.googleapis.com/{ver}/models/{best_model}:generateContent?key={key}"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.post(endpoint, json=payload)
                if res.status_code == 200:
                    gemini_service.active_model = best_model
                    gemini_service.api_version = ver
                    # Save permanently to server .env
                    save_key_to_env(key)
                    return {"valid": True, "model": best_model}
                elif res.status_code in [400, 403]:
                    err_data = res.json()
                    msg = err_data.get("error", {}).get("message", "API key not valid")
                    if "not valid" in msg.lower() or "permission" in msg.lower():
                        return {"valid": False, "error": msg}
        except Exception:
            continue
            
    # Try gemini-2.0-flash direct fallback
    for ver in ["v1beta", "v1"]:
        endpoint = f"https://generativelanguage.googleapis.com/{ver}/models/gemini-2.0-flash:generateContent?key={key}"
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.post(endpoint, json=payload)
                if res.status_code == 200:
                    gemini_service.active_model = "gemini-2.0-flash"
                    gemini_service.api_version = ver
                    save_key_to_env(key)
                    return {"valid": True, "model": "gemini-2.0-flash"}
        except Exception:
            continue

    return {"valid": False, "error": f"Model {best_model} could not be activated. Check API permissions in Google AI Studio."}

@router.post("/", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user_optional)
):
    # Auto-save API key if provided in request
    if request.gemini_api_key and request.gemini_api_key.strip():
        save_key_to_env(request.gemini_api_key.strip())

    # If authenticated, enrich profile with saved user profile from database
    if current_user and current_user.get("sub"):
        try:
            async with aiosqlite.connect(settings.DATABASE_PATH) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute("SELECT profile_data FROM users WHERE id = ?", (current_user["sub"],))
                row = await cursor.fetchone()
                if row and row["profile_data"]:
                    db_profile = json.loads(row["profile_data"])
                    merged = dict(db_profile)
                    if request.profile_updates:
                        merged.update({k: v for k, v in request.profile_updates.items() if v is not None})
                    request.profile_updates = merged
        except Exception:
            pass

    return await assistant_service.process_query(request)
