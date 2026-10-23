from typing import Any, Optional
from pydantic import BaseModel, Field
from app.models.scheme import SchemeResponse
from app.models.session import UserProfile

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    language: Optional[str] = None  # ta, en, tanglish
    profile_updates: Optional[dict[str, Any]] = None
    gemini_api_key: Optional[str] = None
    history: Optional[list[dict[str, Any]]] = None

class EligibilityCheckRequest(BaseModel):
    scheme_id: str
    profile: UserProfile

class EligibilityCheckResponse(BaseModel):
    scheme_id: str
    status: str  # ELIGIBLE, POTENTIALLY_ELIGIBLE, NOT_APPEARING_ELIGIBLE, INSUFFICIENT_INFORMATION
    matched_criteria: list[str]
    unmet_criteria: list[str]
    missing_criteria: list[str]
    reasoning_tamil: str
    reasoning_english: str
    confidence: str = "HIGH"  # HIGH, MEDIUM, LOW

class QueryResponse(BaseModel):
    response_text_tamil: str
    response_text_english: str
    detected_language: str
    detected_intent: str
    extracted_entities: dict[str, Any]
    schemes: list[SchemeResponse]
    eligibility_summaries: list[EligibilityCheckResponse]
    missing_info_prompts: list[str]
    official_sources: list[dict[str, str]]
    audio_base64: Optional[str] = None
