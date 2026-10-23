from typing import Any, Optional
from pydantic import BaseModel, Field

class EligibilityRules(BaseModel):
    model_config = {"extra": "allow"}

    age: Optional[dict[str, Optional[int]]] = None
    gender: Optional[Any] = Field(default_factory=lambda: ["Any"])
    income_limit_annual: Optional[float] = None
    residence: Optional[str] = "Tamil Nadu"
    community: Optional[Any] = Field(default_factory=lambda: ["Any"])
    student_status: Optional[bool] = None
    education_level: Optional[Any] = None
    education: Optional[Any] = None
    schooling_requirement: Optional[str] = None
    school_type: Optional[Any] = None
    employment_status: Optional[str] = None
    occupation: Optional[Any] = None
    marital_status: Optional[Any] = None
    disability: Optional[Any] = None
    disability_percentage: Optional[dict[str, Optional[float]]] = None
    land_limit_wetland_acres: Optional[float] = None
    land_limit_dryland_acres: Optional[float] = None
    electricity_consumption_annual_units: Optional[int] = None
    housing_status: Optional[Any] = None
    location_type: Optional[Any] = None
    special_conditions: Optional[list[str]] = Field(default_factory=list)

class SchemeBase(BaseModel):
    scheme_id: str
    scheme_name_tamil: str
    scheme_name_english: str
    department: str
    department_tamil: Optional[str] = None
    category: str
    sub_category: Optional[str] = None
    description_tamil: str
    description_english: str
    benefits: dict[str, Any]
    eligibility_rules: EligibilityRules
    required_documents: list[str]
    application_method: str
    application_steps: list[str]
    official_urls: list[str]
    contact_helpline: Optional[str] = None
    dates: Optional[dict[str, Any]] = None
    source_metadata: dict[str, Any]
    content_hash: Optional[str] = None
    version: int = 1
    status: str = "Active"

class SchemeResponse(SchemeBase):
    relevance_score: Optional[float] = None
    eligibility_status: Optional[str] = None
    matched_criteria: Optional[list[str]] = None
    unmet_criteria: Optional[list[str]] = None
    missing_criteria: Optional[list[str]] = None
