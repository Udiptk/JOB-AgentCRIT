from fastapi import APIRouter
from app.schemas.application import ApplicationCreate

router = APIRouter()

@router.post("/")
async def apply_to_job(application: ApplicationCreate):
    return {"message": "Application submitted."}

@router.get("/{user_id}")
async def list_applications(user_id: int):
    return {"applications": []}
