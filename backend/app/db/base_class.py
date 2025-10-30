"""Base class for declarative SQLAlchemy models."""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr


class Base(DeclarativeBase):
    id: Mapped[int]

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower()

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        attrs = (
            f"{name}={getattr(self, name)!r}"
            for name in self.__mapper__.columns.keys()  # type: ignore[attr-defined]
        )
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def dict(self) -> dict[str, Any]:
        return {col.key: getattr(self, col.key) for col in self.__table__.columns}
