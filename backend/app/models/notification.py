"""Notification model."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class NotificationChannel(str, Enum):
    SMS = "sms"
    EMAIL = "email"
    TELEGRAM = "telegram"


class NotificationStatus(str, Enum):
    SENT = "sent"
    FAILED = "failed"
    QUEUED = "queued"


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    channel: Mapped[NotificationChannel] = mapped_column(Enum(NotificationChannel))
    template_key: Mapped[str] = mapped_column(String(50))
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[NotificationStatus] = mapped_column(Enum(NotificationStatus), default=NotificationStatus.QUEUED)
    cost: Mapped[float | None] = mapped_column(nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="notifications")
