"""
LangGraph Transition Logic — conditional edges that control pipeline flow.
"""
from app.orchestration.state import JobAgentState


def should_generate_resume(state: JobAgentState) -> str:
    """Only generate resume if profile is loaded."""
    if state.get("profile"):
        return "generate_resume"
    return "error"


def should_score_ats(state: JobAgentState) -> str:
    """Only score ATS if resume exists."""
    if state.get("resume_md"):
        return "score_ats"
    return "error"


def should_hunt_jobs(state: JobAgentState) -> str:
    """Always hunt jobs after resume is ready."""
    if state.get("profile") and state.get("resume_md"):
        return "hunt_jobs"
    return "error"


def should_rank(state: JobAgentState) -> str:
    """Only rank if we have jobs."""
    if state.get("raw_jobs"):
        return "rank_jobs"
    return "notify"


def should_apply(state: JobAgentState) -> str:
    """Only auto-apply if ranked jobs exist."""
    if state.get("ranked_jobs"):
        return "auto_apply"
    return "notify"
