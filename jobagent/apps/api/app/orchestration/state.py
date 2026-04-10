"""
LangGraph Agent State — shared state object flowing through the entire pipeline.
"""
from typing import TypedDict, Optional, List, Annotated
import operator


class JobAgentState(TypedDict):
    """
    Shared state that flows through every node in the LangGraph pipeline.
    Each agent reads from and writes to this state.
    """
    # Identity
    user_id: int

    # Profile
    profile: Optional[dict]

    # Resume
    resume_md: Optional[str]
    resume_json: Optional[dict]
    ats_score: Optional[float]
    keywords_matched: List[str]
    keywords_missing: List[str]
    resume_suggestions: List[str]

    # Jobs
    raw_jobs: List[dict]                  # All scraped jobs
    ranked_jobs: List[dict]               # Top-N after ranking

    # Applications
    applications: Annotated[List[dict], operator.add]   # Append-safe

    # Notifications
    notifications: Annotated[List[dict], operator.add]  # Append-safe

    # Pipeline control
    current_step: str
    errors: Annotated[List[str], operator.add]
    completed_steps: Annotated[List[str], operator.add]

    # Search params
    search_query: Optional[str]
    target_location: Optional[str]
    sources: List[str]
