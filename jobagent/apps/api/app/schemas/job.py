from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class JobSearchRequest(BaseModel):
    user_id: int
    keywords: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    sources: List[str] = ["linkedin", "indeed", "naukri"]


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: Optional[str]
    job_type: Optional[str]
    salary_range: Optional[str]
    description: Optional[str]
    source: str
    source_url: Optional[str]
    match_score: Optional[float]
    match_reasons: List[str] = []
    missing_skills: List[str] = []
    posted_at: Optional[datetime]
    scraped_at: datetime

    class Config:
        from_attributes = True


class JobRankingOut(BaseModel):
    jobs: List[JobOut]
    total: int
    user_id: int
