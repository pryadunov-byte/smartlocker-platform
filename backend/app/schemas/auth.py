"""Authentication and user schemas."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr

from ..models.user import UserRole


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    phone: str | None


class UserCreate(BaseModel):
    email: EmailStr
    role: UserRole
    phone: str | None = None
    password: str


class UserUpdate(BaseModel):
    role: UserRole | None = None
    phone: str | None = None
    password: str | None = None
