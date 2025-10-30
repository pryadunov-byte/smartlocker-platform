"""Authentication endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ...core import security
from ...core.config import settings
from ...models.user import UserRole
from ...schemas import auth as schemas
from ...services.users import UsersService
from ..deps import get_db_session, get_current_user

router = APIRouter()


@router.post("/token", response_model=schemas.TokenPair)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db_session)):
    service = UsersService(session)
    user = await service.get_by_email(form_data.username)
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access = security.create_access_token(str(user.id))
    refresh = security.create_refresh_token(str(user.id))
    return schemas.TokenPair(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=schemas.TokenPair)
async def refresh_token(payload: schemas.RefreshRequest, session: AsyncSession = Depends(get_db_session)):
    data = security.verify_token(payload.refresh_token, settings.JWT_REFRESH_SECRET_KEY)
    user_id = data.get("sub")
    service = UsersService(session)
    user = await service.get(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    access = security.create_access_token(str(user.id))
    refresh = security.create_refresh_token(str(user.id))
    return schemas.TokenPair(access_token=access, refresh_token=refresh)


@router.get("/me", response_model=schemas.UserOut)
async def me(user=Depends(get_current_user)):
    return schemas.UserOut(id=user.id, email=user.email, role=user.role, phone=user.phone)


@router.post("/seed-admin", include_in_schema=False)
async def seed_admin(session: AsyncSession = Depends(get_db_session)):
    service = UsersService(session)
    existing = await service.get_by_email("admin@demo.local")
    if existing:
        return {"created": False}
    await service.create("admin@demo.local", "Admin123!", UserRole.ADMIN)
    return {"created": True}
