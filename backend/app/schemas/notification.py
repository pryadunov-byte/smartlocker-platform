"""Notification DTOs."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.notification import NotificationChannel, NotificationStatus


class NotificationOut(BaseModel):
    id: int
    order_id: int
    channel: NotificationChannel
    template_key: str
    sent_at: Optional[datetime]
    status: NotificationStatus
    cost: Optional[float]


class NotificationCreate(BaseModel):
    order_id: int
    channel: NotificationChannel
    template_key: str
