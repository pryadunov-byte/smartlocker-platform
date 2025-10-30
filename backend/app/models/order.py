"""Order domain model."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class OrderType(str, Enum):
    DELIVERY = "delivery"
    RETURN = "return"
    RENT = "rent"
    STORAGE = "storage"


class OrderStatus(str, Enum):
    CREATED = "created"
    AWAITING_PICKUP = "awaiting_pickup"
    PICKED_UP = "picked_up"
    OVERDUE = "overdue"
    RETURNED = "returned"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    public_uid: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"))
    cell_id: Mapped[int | None] = mapped_column(ForeignKey("locker_cells.id"), nullable=True)
    type: Mapped[OrderType] = mapped_column(Enum(OrderType))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.CREATED)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    picked_up_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scenario_id: Mapped[int | None] = mapped_column(ForeignKey("scenarios.id"), nullable=True)
    payload: Mapped[dict[str, str] | None] = mapped_column(JSONB, default=dict)

    device: Mapped["Device"] = relationship("Device", back_populates="orders")
    cell: Mapped["LockerCell"] = relationship("LockerCell", back_populates="orders")
    access_code: Mapped["AccessCode"] = relationship("AccessCode", back_populates="order", uselist=False, cascade="all, delete-orphan")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="order")
    scenario: Mapped["Scenario"] = relationship("Scenario", back_populates="orders")
