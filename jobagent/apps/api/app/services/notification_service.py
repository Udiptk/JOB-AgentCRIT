"""
Notification Service — creates and persists notification records.
"""
from datetime import datetime
from loguru import logger


async def create_notification(
    user_id: int,
    type: str,
    title: str,
    message: str,
    agent: str = None,
    metadata: dict = None,
) -> dict:
    """
    Create a notification record and return it.
    In production: persists to DB via NotificationRepository.
    """
    notif = {
        "user_id": user_id,
        "type": type,
        "title": title,
        "message": message,
        "agent": agent,
        "metadata": metadata or {},
        "is_read": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    logger.info(f"[NotificationService] {type} | {title}: {message}")
    return notif


async def mark_all_read(user_id: int):
    """Mark all notifications as read for a user."""
    # TODO: DB update
    logger.info(f"[NotificationService] Marked all read for user {user_id}")
