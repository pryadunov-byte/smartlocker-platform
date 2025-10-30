"""Access code data model."""
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class AccessCode(Base):
    __tablename__ = "access_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), unique=True)
    pin_hash: Mapped[str] = mapped_column(String(128))
    qr_token: Mapped[str] = mapped_column(String(256))
    attempts_left: Mapped[int] = mapped_column(Integer, default=3)

    order: Mapped["Order"] = relationship("Order", back_populates="access_code")
