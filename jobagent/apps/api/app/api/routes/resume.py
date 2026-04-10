from fastapi import APIRouter
from app.schemas.resume import ResumeGenerateRequest

router = APIRouter()

@router.post("/generate")
async def generate_resume(request: ResumeGenerateRequest):
    return {"message": "Resume generation triggered."}

@router.get("/{user_id}")
async def get_resumes(user_id: int):
    return {"resumes": []}
