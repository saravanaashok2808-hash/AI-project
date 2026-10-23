from fastapi import APIRouter, HTTPException
from app.models.query import EligibilityCheckRequest, EligibilityCheckResponse
from app.services.scheme_service import scheme_service
from app.eligibility.rule_evaluator import EligibilityEngine
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=EligibilityCheckResponse)
async def check_eligibility(request: EligibilityCheckRequest):
    scheme_dict = await scheme_service.get_scheme(request.scheme_id)
    if not scheme_dict:
        raise HTTPException(status_code=404, detail="Scheme not found")
        
    result = EligibilityEngine.evaluate(request.profile, scheme_dict)
    
    return EligibilityCheckResponse(
        scheme_id=result.scheme_id,
        status=result.status,
        matched_criteria=result.matched_criteria,
        unmet_criteria=result.unmet_criteria,
        missing_criteria=result.missing_criteria,
        reasoning_tamil=result.reasoning_tamil,
        reasoning_english=result.reasoning_english,
        confidence=result.confidence
    )
