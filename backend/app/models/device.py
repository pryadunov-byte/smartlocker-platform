"""SQLAlchemy model for smart locker devices."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    geo_lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    geo_lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status_online: Mapped[bool] = mapped_column(Boolean, default=True)
    firmware: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    addr: Mapped[int] = mapped_column(Integer, default=0)
    baud: Mapped[int] = mapped_column(Integer, default=19200)
    max_boards: Mapped[int] = mapped_column(Integer, default=16)
    extra: Mapped[dict | None] = mapped_column(JSONB, default=dict)

    cells: Mapped[list["LockerCell"]] = relationship("LockerCell", back_populates="device", cascade="all, delete-orphan")
    alerts: Mapped[list["Alert"]] = relationship("Alert", back_populates="device", cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="device")
