"""Scenario model storing configurable workflow parameters."""
from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    params_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="scenario")
