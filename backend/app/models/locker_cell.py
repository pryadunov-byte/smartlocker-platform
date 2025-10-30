"""Locker cell model definition."""
from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class LockerCellStatus(str, Enum):
    FREE = "free"
    OCCUPIED = "occupied"
    FAULT = "fault"
    DIRTY = "dirty"
    OPEN = "open"


class LockerCell(Base):
    __tablename__ = "locker_cells"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(String(10))
    size: Mapped[str] = mapped_column(String(32))
    status: Mapped[LockerCellStatus] = mapped_column(Enum(LockerCellStatus), default=LockerCellStatus.FREE)
    cooled: Mapped[bool] = mapped_column(Boolean, default=False)
    needs_repair: Mapped[bool] = mapped_column(Boolean, default=False)
    open: Mapped[bool] = mapped_column(Boolean, default=False)
    flags: Mapped[Optional[dict[str, bool]]] = mapped_column(JSONB, default=dict)
    services_enabled: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    device: Mapped["Device"] = relationship("Device", back_populates="cells")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="cell")
