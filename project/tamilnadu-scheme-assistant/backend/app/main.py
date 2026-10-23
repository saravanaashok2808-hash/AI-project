from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.schemes import router as schemes_router
from app.api.query import router as query_router
from app.api.eligibility import router as eligibility_router
from app.api.voice import router as voice_router

import threading
from app.ai.llm.raw_model import llm_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database & Load LLM onto GPU
    await init_db()
    threading.Thread(target=llm_service.load_model, daemon=True).start()
    yield
    # Shutdown

app = FastAPI(title="Tamil Nadu Scheme Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(schemes_router, prefix="/api/schemes", tags=["schemes"])
app.include_router(query_router, prefix="/api/query", tags=["query"])
app.include_router(eligibility_router, prefix="/api/eligibility", tags=["eligibility"])
app.include_router(voice_router, prefix="/api/voice", tags=["voice"])

