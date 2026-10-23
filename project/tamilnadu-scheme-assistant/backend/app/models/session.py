from typing import Optional
from pydantic import BaseModel, Field

class UserProfile(BaseModel):
    model_config = {"extra": "allow"}

    age: Optional[int] = None
    gender: Optional[str] = None  # Female, Male, Transgender
    district: Optional[str] = None
    residence: Optional[str] = "Tamil Nadu"
    area_type: Optional[str] = None  # Rural, Urban
    annual_income: Optional[float] = None
    community: Optional[str] = None  # SC, ST, BC, MBC, General
    occupation: Optional[str] = None  # Farmer, Agricultural Laborer, Student, Unemployed, etc.
    employment_status: Optional[str] = None
    student_status: Optional[bool] = None
    education_level: Optional[str] = None
    schooling_type: Optional[str] = None  # Government School, Private School
    marital_status: Optional[str] = None  # Married, Single, Widow, Remarried
    is_differently_abled: Optional[bool] = None
    disability_percentage: Optional[float] = None
    land_holding_acres: Optional[float] = None
    electricity_units_annual: Optional[int] = None
    ration_card_type: Optional[str] = None  # PHH, NPHH, AAY
    preferred_language: str = "Tamil"  # Tamil, English, Tanglish

class SessionState(BaseModel):
    session_id: str
    profile: UserProfile = Field(default_factory=UserProfile)
    conversation_history: list[dict[str, str]] = Field(default_factory=list)
    last_retrieved_schemes: list[str] = Field(default_factory=list)
    pending_follow_ups: list[str] = Field(default_factory=list)
