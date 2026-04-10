"""
LangGraph Node Functions — each node wraps an agent call.
"""
from loguru import logger
from app.orchestration.state import JobAgentState
from app.agents import (
    profile_agent,
    resume_agent,
    ats_agent,
    job_hunter_agent,
    ranking_agent,
    cover_letter_agent,
    auto_apply_agent,
    tracker_agent,
    notifier_agent,
)


async def node_load_profile(state: JobAgentState) -> dict:
    logger.info(f"[Node] load_profile | user_id={state['user_id']}")
    result = await profile_agent.run(state)
    return {
        "profile": result["profile"],
        "current_step": "load_profile",
        "completed_steps": ["load_profile"],
        "notifications": [{
            "type": "agent_update",
            "title": "Profile Agent",
            "message": "Profile loaded successfully.",
            "agent": "profile_agent",
        }],
    }


async def node_generate_resume(state: JobAgentState) -> dict:
    logger.info(f"[Node] generate_resume | user_id={state['user_id']}")
    result = await resume_agent.run(state)
    return {
        "resume_md": result["resume_md"],
        "resume_json": result["resume_json"],
        "current_step": "generate_resume",
        "completed_steps": ["generate_resume"],
        "notifications": [{
            "type": "agent_update",
            "title": "Resume Agent",
            "message": "ATS-optimized resume generated.",
            "agent": "resume_agent",
        }],
    }


async def node_score_ats(state: JobAgentState) -> dict:
    logger.info(f"[Node] score_ats | user_id={state['user_id']}")
    result = await ats_agent.run(state)
    return {
        "ats_score": result["ats_score"],
        "keywords_matched": result["keywords_matched"],
        "keywords_missing": result["keywords_missing"],
        "resume_suggestions": result["suggestions"],
        "current_step": "score_ats",
        "completed_steps": ["score_ats"],
        "notifications": [{
            "type": "agent_update",
            "title": "ATS Agent",
            "message": f"ATS Score: {result['ats_score']:.0f}/100",
            "agent": "ats_agent",
        }],
    }


async def node_hunt_jobs(state: JobAgentState) -> dict:
    logger.info(f"[Node] hunt_jobs | user_id={state['user_id']}")
    result = await job_hunter_agent.run(state)
    count = len(result["raw_jobs"])
    return {
        "raw_jobs": result["raw_jobs"],
        "current_step": "hunt_jobs",
        "completed_steps": ["hunt_jobs"],
        "notifications": [{
            "type": "job_found",
            "title": "Job Hunter Agent",
            "message": f"Found {count} jobs across {len(state['sources'])} platforms.",
            "agent": "job_hunter_agent",
        }],
    }


async def node_rank_jobs(state: JobAgentState) -> dict:
    logger.info(f"[Node] rank_jobs | user_id={state['user_id']}")
    result = await ranking_agent.run(state)
    return {
        "ranked_jobs": result["ranked_jobs"],
        "current_step": "rank_jobs",
        "completed_steps": ["rank_jobs"],
        "notifications": [{
            "type": "agent_update",
            "title": "Ranking Agent",
            "message": f"Top {len(result['ranked_jobs'])} jobs ranked by match score.",
            "agent": "ranking_agent",
        }],
    }


async def node_auto_apply(state: JobAgentState) -> dict:
    logger.info(f"[Node] auto_apply | user_id={state['user_id']}")
    result = await auto_apply_agent.run(state)
    return {
        "applications": result["applications"],
        "current_step": "auto_apply",
        "completed_steps": ["auto_apply"],
        "notifications": [{
            "type": "applied",
            "title": "Auto Apply Agent",
            "message": f"Applied to {len(result['applications'])} jobs.",
            "agent": "auto_apply_agent",
        }],
    }


async def node_notify(state: JobAgentState) -> dict:
    logger.info(f"[Node] notify | user_id={state['user_id']}")
    await notifier_agent.run(state)
    return {
        "current_step": "notify",
        "completed_steps": ["notify"],
    }
