import sys
import uuid
import secrets
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.main import app

def test_register_and_login():
    with TestClient(app) as client:
        unique_phone = f"9{secrets.randbelow(899999999) + 100000000}"
        unique_name = f"Citizen_{uuid.uuid4().hex[:6]}"
        reg_payload = {
            "name": unique_name,
            "password": "SecretPassword123",
            "phone": unique_phone,
            "age": 28,
            "gender": "Male",
            "district": "Madurai",
            "profile_data": {
                "education_level": "Graduate",
                "employment_status": "Unemployed"
            }
        }
        
        # 1. Register
        reg_res = client.post("/api/auth/register", json=reg_payload)
        assert reg_res.status_code == 200, reg_res.text
        data = reg_res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["name"] == unique_name
        assert data["user"]["profile"]["age"] == 28

        token = data["access_token"]

        # 2. Duplicate registration with same phone must fail
        dup_res = client.post("/api/auth/register", json=reg_payload)
        assert dup_res.status_code == 400

        # 3. Login with correct credentials
        login_res = client.post("/api/auth/login", json={
            "identifier": unique_phone,
            "password": "SecretPassword123"
        })
        assert login_res.status_code == 200
        login_data = login_res.json()
        assert "access_token" in login_data
        assert login_data["user"]["name"] == unique_name

        # 4. Login with incorrect password must fail with 401
        bad_res = client.post("/api/auth/login", json={
            "identifier": unique_phone,
            "password": "WrongPassword"
        })
        assert bad_res.status_code == 401

        # 5. Access protected /api/auth/me with Bearer token
        me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        assert me_res.json()["name"] == unique_name

        # 6. Access protected /api/auth/me without token must fail with 401
        unauth_res = client.get("/api/auth/me")
        assert unauth_res.status_code == 401

def test_security_headers():
    with TestClient(app) as client:
        res = client.get("/api/health")
        assert res.status_code == 200
        assert res.headers.get("X-Content-Type-Options") == "nosniff"
        assert res.headers.get("X-Frame-Options") == "DENY"
        assert res.headers.get("X-XSS-Protection") == "1; mode=block"
