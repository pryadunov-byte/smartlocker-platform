"""Notification service with cost tracking."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.notification import Notification, NotificationChannel, NotificationStatus

CHANNEL_COSTS = {
    NotificationChannel.SMS: 2.5,
    NotificationChannel.EMAIL: 0.2,
    NotificationChannel.TELEGRAM: 0.05,
}


class NotificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, order_id: int | None = None) -> Iterable[Notification]:
        query = select(Notification)
        if order_id:
            query = query.where(Notification.order_id == order_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, order_id: int, channel: NotificationChannel, template_key: str) -> Notification:
        notification = Notification(
            order_id=order_id,
            channel=channel,
            template_key=template_key,
            status=NotificationStatus.QUEUED,
            cost=CHANNEL_COSTS.get(channel, 0),
        )
        self.session.add(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def mark_sent(self, notification: Notification) -> Notification:
        notification.status = NotificationStatus.SENT
        notification.sent_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(notification)
        return notification
