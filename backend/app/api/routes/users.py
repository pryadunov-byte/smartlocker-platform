"""User management endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.user import UserRole
from ...schemas.auth import UserCreate, UserOut, UserUpdate
from ...services.users import UsersService
from ..deps import get_db_session, require_roles

router = APIRouter(dependencies=[Depends(require_roles(UserRole.ADMIN))])


@router.get("/", response_model=list[UserOut])
async def list_users(session: AsyncSession = Depends(get_db_session)):
    service = UsersService(session)
    users = await service.list()
    return [UserOut(id=user.id, email=user.email, role=user.role, phone=user.phone) for user in users]


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_db_session)):
    service = UsersService(session)
    existing = await service.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await service.create(payload.email, payload.password, payload.role, payload.phone)
    return UserOut(id=user.id, email=user.email, role=user.role, phone=user.phone)


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, payload: UserUpdate, session: AsyncSession = Depends(get_db_session)):
    service = UsersService(session)
    user = await service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await service.update(user, password=payload.password, role=payload.role, phone=payload.phone)
    return UserOut(id=user.id, email=user.email, role=user.role, phone=user.phone)
