from fastapi import APIRouter

router = APIRouter()

@router.get("/{user_id}")
async def list_notifications(user_id: int):
    return {"notifications": []}

@router.post("/{user_id}/read")
async def mark_read(user_id: int):
    return {"message": "Notifications marked as read."}
