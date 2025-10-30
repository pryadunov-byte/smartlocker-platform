"""Notification endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.notification import NotificationCreate, NotificationOut
from ...services.notifications import NotificationService
from ..deps import get_db_session, require_roles

router = APIRouter(dependencies=[Depends(require_roles())])


@router.get("/", response_model=list[NotificationOut])
async def list_notifications(session: AsyncSession = Depends(get_db_session)):
    service = NotificationService(session)
    notifications = await service.list()
    return [
        NotificationOut(
            id=item.id,
            order_id=item.order_id,
            channel=item.channel,
            template_key=item.template_key,
            sent_at=item.sent_at,
            status=item.status,
            cost=item.cost,
        )
        for item in notifications
    ]


@router.post("/", response_model=NotificationOut, status_code=201)
async def create_notification(payload: NotificationCreate, session: AsyncSession = Depends(get_db_session)):
    service = NotificationService(session)
    notification = await service.create(payload.order_id, payload.channel, payload.template_key)
    return NotificationOut(
        id=notification.id,
        order_id=notification.order_id,
        channel=notification.channel,
        template_key=notification.template_key,
        sent_at=notification.sent_at,
        status=notification.status,
        cost=notification.cost,
    )
