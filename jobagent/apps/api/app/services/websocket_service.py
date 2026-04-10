"""
WebSocket Service — manages active connections and broadcasts messages.
"""
import json
from typing import Dict, List
from fastapi import WebSocket
from loguru import logger


class ConnectionManager:
    def __init__(self):
        # user_id → list of WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"[WS] User {user_id} connected. Total: {len(self.active_connections[user_id])}")

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        logger.info(f"[WS] User {user_id} disconnected.")

    async def send_to_user(self, user_id: int, message: dict):
        connections = self.active_connections.get(user_id, [])
        dead = []
        for ws in connections:
            try:
                await ws.send_text(json.dumps(message))
            except Exception as e:
                logger.warning(f"[WS] Failed to send to user {user_id}: {e}")
                dead.append(ws)
        for ws in dead:
            self.disconnect(user_id, ws)

    async def broadcast(self, message: dict):
        for user_id in list(self.active_connections.keys()):
            await self.send_to_user(user_id, message)


# Global singleton
manager = ConnectionManager()


async def broadcast_to_user(user_id: int, message: dict):
    await manager.send_to_user(user_id, message)


