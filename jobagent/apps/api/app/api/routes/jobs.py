from fastapi import APIRouter, BackgroundTasks
from app.schemas.job import JobSearchRequest
import asyncio
from app.services.websocket_service import broadcast_to_user

router = APIRouter()

async def mock_pipeline(user_id: int):
    await broadcast_to_user(user_id, {"type": "log", "agent": "System", "message": "Pipeline started (MOCKED)."})
    await asyncio.sleep(2)
    await broadcast_to_user(user_id, {"type": "log", "agent": "Resume Agent", "message": "Updated resume."})
    await asyncio.sleep(2)
    await broadcast_to_user(user_id, {"type": "log", "agent": "Ranking Agent", "message": "Found 4 matches."})

@router.post("/hunt")
async def trigger_job_hunt(request: JobSearchRequest, background_tasks: BackgroundTasks):
    """Trigger the LangGraph workflow to hunt jobs."""
    background_tasks.add_task(mock_pipeline, request.user_id)
    return {"message": "Job hunt pipeline started. Listen to WebSockets for updates."}

@router.get("/")
async def list_jobs(user_id: int):
    return {"jobs": []}
