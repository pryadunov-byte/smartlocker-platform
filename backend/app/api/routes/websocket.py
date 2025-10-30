"""Realtime WebSocket endpoints."""
from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ...websocket.events import manager

router = APIRouter()


@router.websocket("/alerts")
async def websocket_alerts(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_json()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
