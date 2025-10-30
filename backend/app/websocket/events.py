"""WebSocket manager for realtime alerts."""
from __future__ import annotations

from typing import Set

from fastapi import WebSocket


class AlertsWebSocketManager:
    def __init__(self) -> None:
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.discard(websocket)

    async def broadcast(self, message: dict) -> None:
        for connection in set(self.connections):
            await connection.send_json(message)


manager = AlertsWebSocketManager()
