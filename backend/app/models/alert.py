"""Alert model representing device incidents."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertKind(str, Enum):
    OFFLINE = "offline"
    LOCK_FAULT = "lock_fault"
    OVERHEAT = "overheat"
    DIRTY = "dirty"
    CAPACITY = "capacity"
    OTHER = "other"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id", ondelete="CASCADE"))
    severity: Mapped[AlertSeverity] = mapped_column(Enum(AlertSeverity))
    kind: Mapped[AlertKind] = mapped_column(Enum(AlertKind))
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    device: Mapped["Device"] = relationship("Device", back_populates="alerts")
