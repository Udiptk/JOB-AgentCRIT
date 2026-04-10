from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime


class AgentState(BaseModel):
    """Shared state that flows through the LangGraph pipeline."""
    user_id: int
    profile: Optional[dict] = None
    resume: Optional[dict] = None
    jobs: List[dict] = []
    ranked_jobs: List[dict] = []
    applications: List[dict] = []
    notifications: List[dict] = []
    current_agent: Optional[str] = None
    errors: List[str] = []
    metadata: dict = {}
