from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str

@router.get("/")
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", version="1.0.0")
