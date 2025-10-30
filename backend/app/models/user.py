"""User and role model."""
from __future__ import annotations

from enum import Enum

from sqlalchemy import Enum as SqlEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base_class import Base


class UserRole(str, Enum):
    ADMIN = "administrator"
    OPERATOR = "operator"
    TECHNICIAN = "technician"
    COURIER = "courier"
    ANALYST = "analyst"
    CLIENT = "client"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="actor")
