from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger
from app.services.websocket_service import manager


router = APIRouter()

@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            # We don't expect much client->server over WS, primarily server->client streaming
            data = await websocket.receive_text()
            logger.debug(f"[WS] User {user_id} sent: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
