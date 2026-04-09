from datetime import datetime
from typing import Optional
import json

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Profile fields
    headline: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # JSON fields stored as text
    skills_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)      # ["Python", "React"]
    experience_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # [{...}, {...}]
    education_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)   # [{...}]
    projects_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)    # [{...}]

    # Preferences
    target_roles_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_locations_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    salary_min: Mapped[Optional[int]] = mapped_column(nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(nullable=True)
    dream_companies_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    applications: Mapped[list["Application"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @property
    def skills(self):
        return json.loads(self.skills_json) if self.skills_json else []

    @property
    def experience(self):
        return json.loads(self.experience_json) if self.experience_json else []

    @property
    def projects(self):
        return json.loads(self.projects_json) if self.projects_json else []
