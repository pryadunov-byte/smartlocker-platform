"""Alert endpoints for monitoring."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.alert import AlertCreate, AlertOut
from ...services.alerts import AlertsService
from ..deps import get_db_session, require_roles

router = APIRouter(dependencies=[Depends(require_roles())])


@router.get("/", response_model=list[AlertOut])
async def list_alerts(session: AsyncSession = Depends(get_db_session)):
    service = AlertsService(session)
    alerts = await service.list()
    return [
        AlertOut(
            id=item.id,
            device_id=item.device_id,
            severity=item.severity,
            kind=item.kind,
            message=item.message,
            created_at=item.created_at,
            resolved_at=item.resolved_at,
        )
        for item in alerts
    ]


@router.post("/", response_model=AlertOut, status_code=201)
async def create_alert(payload: AlertCreate, session: AsyncSession = Depends(get_db_session)):
    service = AlertsService(session)
    alert = await service.create(payload.device_id, payload.severity, payload.kind, payload.message)
    return AlertOut(
        id=alert.id,
        device_id=alert.device_id,
        severity=alert.severity,
        kind=alert.kind,
        message=alert.message,
        created_at=alert.created_at,
        resolved_at=alert.resolved_at,
    )
