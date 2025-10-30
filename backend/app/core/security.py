"""Security helpers for JWT token generation and password hashing."""
from __future__ import annotations

import datetime as dt
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict[str, Any], expires_delta: dt.timedelta, secret: str) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=settings.JWT_ALGORITHM)


def create_access_token(subject: str) -> str:
    return create_token(
        {"sub": subject, "type": "access"},
        dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        settings.JWT_SECRET_KEY,
    )


def create_refresh_token(subject: str) -> str:
    return create_token(
        {"sub": subject, "type": "refresh"},
        dt.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        settings.JWT_REFRESH_SECRET_KEY,
    )


def verify_token(token: str, secret: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)
