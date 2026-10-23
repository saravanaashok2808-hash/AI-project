import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DATABASE_PATH: Path = BASE_DIR / os.getenv("DATABASE_PATH", "data/schemes.db")
    CHROMA_PERSIST_DIR: Path = BASE_DIR / os.getenv("CHROMA_PERSIST_DIR", "../data/chroma_db")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
    ]
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Google Gemini AI API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # API Security and JWT Authentication
    JWT_SECRET: str = os.getenv("JWT_SECRET", "tn_scheme_assistant_secure_jwt_secret_key_2026_gov")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7
    API_KEY_HEADER: str = "X-API-Key"
    REQUIRED_API_KEY: str = os.getenv("REQUIRED_API_KEY", "")
    
    # Official trusted government domains for Tamil Nadu
    OFFICIAL_DOMAIN_ALLOWLIST: list[str] = [
        "tn.gov.in",
        "tnesevai.tn.gov.in",
        "cmhelpline.tn.gov.in",
        "kmut.tn.gov.in",
        "penkalvi.tn.gov.in",
        "cmchistn.com",
        "scd.tn.gov.in",
        "tahdco.tn.gov.in",
        "tnvelaivaaippu.gov.in",
        "cms.tn.gov.in",
        "myscheme.gov.in",
        "india.gov.in"
    ]

settings = Settings()
