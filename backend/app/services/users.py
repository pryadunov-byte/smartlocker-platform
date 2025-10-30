"""User domain service."""
from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import security
from ..models.user import User, UserRole


class UsersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, email: str, password: str, role: UserRole, phone: str | None = None) -> User:
        user = User(email=email, password_hash=security.hash_password(password), role=role, phone=phone)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, *, password: str | None = None, role: UserRole | None = None, phone: str | None = None) -> User:
        if password:
            user.password_hash = security.hash_password(password)
        if role:
            user.role = role
        if phone is not None:
            user.phone = phone
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def list(self) -> Iterable[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()
