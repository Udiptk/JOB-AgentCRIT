from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class ApplicationCreate(BaseModel):
    user_id: int
    job_id: int
    resume_id: Optional[int] = None
    auto_generate_cover_letter: bool = True


class ApplicationOut(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    cover_letter: Optional[str]
    notes: Optional[str]
    applied_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None
