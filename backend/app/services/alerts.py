"""Alert service for realtime monitoring."""
from __future__ import annotations

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.alert import Alert, AlertKind, AlertSeverity
from ..websocket.events import manager


class AlertsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> Iterable[Alert]:
        result = await self.session.execute(select(Alert))
        return result.scalars().all()

    async def create(self, device_id: int, severity: AlertSeverity, kind: AlertKind, message: str | None) -> Alert:
        alert = Alert(device_id=device_id, severity=severity, kind=kind, message=message)
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        await manager.broadcast(
            {
                "type": "alert",
                "id": alert.id,
                "device_id": alert.device_id,
                "severity": alert.severity.value,
                "kind": alert.kind.value,
                "message": alert.message,
                "created_at": alert.created_at.isoformat(),
            }
        )
        return alert
