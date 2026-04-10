"""
Pipeline Runner — executes the LangGraph pipeline and streams events via WebSocket.
"""
from loguru import logger
from app.orchestration.graph import jobagent_graph
from app.orchestration.state import JobAgentState
from app.services.websocket_service import broadcast_to_user


async def run_pipeline(
    user_id: int,
    search_query: str = None,
    target_location: str = None,
    sources: list = None,
    auto_apply: bool = False,
) -> dict:
    """
    Run the full JOBAGENT pipeline for a user.
    Streams progress back via WebSocket in real time.
    """
    initial_state: JobAgentState = {
        "user_id": user_id,
        "profile": None,
        "resume_md": None,
        "resume_json": None,
        "ats_score": None,
        "keywords_matched": [],
        "keywords_missing": [],
        "resume_suggestions": [],
        "raw_jobs": [],
        "ranked_jobs": [],
        "applications": [],
        "notifications": [],
        "current_step": "start",
        "errors": [],
        "completed_steps": [],
        "search_query": search_query,
        "target_location": target_location,
        "sources": sources or ["linkedin", "indeed", "naukri"],
    }

    logger.info(f"Starting JOBAGENT pipeline for user_id={user_id}")

    async for event in jobagent_graph.astream(initial_state):
        for node_name, output in event.items():
            logger.info(f"[Pipeline] Node '{node_name}' completed")

            # Stream new notifications via WebSocket
            notifications = output.get("notifications", [])
            for notif in notifications:
                await broadcast_to_user(user_id, {
                    "type": "agent_event",
                    "node": node_name,
                    **notif,
                })

    logger.info(f"JOBAGENT pipeline complete for user_id={user_id}")
    return {"status": "complete", "user_id": user_id}
