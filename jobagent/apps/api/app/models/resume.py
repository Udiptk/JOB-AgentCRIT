from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    title: Mapped[str] = mapped_column(String(255), default="My Resume")
    content_md: Mapped[Optional[str]] = mapped_column(Text, nullable=True)     # Markdown resume
    content_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)   # Structured JSON
    pdf_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ATS fields
    ats_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    keywords_matched_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    keywords_missing_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    suggestions_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Targeting
    target_job_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_job_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="resumes")
