from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ExperienceItem(BaseModel):
    company: str
    role: str
    start_date: str
    end_date: Optional[str] = None
    is_current: bool = False
    description: str


class EducationItem(BaseModel):
    institution: str
    degree: str
    field: str
    start_year: int
    end_year: Optional[int] = None
    gpa: Optional[float] = None


class ProjectItem(BaseModel):
    name: str
    description: str
    tech_stack: List[str] = []
    url: Optional[str] = None


class ProfileCreate(BaseModel):
    email: EmailStr
    name: str
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    experience: List[ExperienceItem] = []
    education: List[EducationItem] = []
    projects: List[ProjectItem] = []
    target_roles: List[str] = []
    target_locations: List[str] = []
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    dream_companies: List[str] = []


class ProfileUpdate(ProfileCreate):
    pass


class ProfileOut(ProfileCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
