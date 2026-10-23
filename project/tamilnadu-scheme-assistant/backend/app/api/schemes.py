from fastapi import APIRouter, HTTPException
from app.services.scheme_service import scheme_service

router = APIRouter()

@router.get("/")
async def get_all_schemes():
    return await scheme_service.get_all_schemes()

@router.get("/{scheme_id}")
async def get_scheme(scheme_id: str):
    scheme = await scheme_service.get_scheme(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme
