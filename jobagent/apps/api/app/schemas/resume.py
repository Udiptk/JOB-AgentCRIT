from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class ResumeGenerateRequest(BaseModel):
    user_id: int
    target_job_title: Optional[str] = None
    target_job_description: Optional[str] = None


class ResumeOut(BaseModel):
    id: int
    user_id: int
    title: str
    content_md: Optional[str]
    ats_score: Optional[float]
    keywords_matched: List[str] = []
    keywords_missing: List[str] = []
    suggestions: List[str] = []
    pdf_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ATSScoreOut(BaseModel):
    score: float
    keywords_matched: List[str]
    keywords_missing: List[str]
    suggestions: List[str]
    coverage_percent: float
