"""Application configuration module."""
from __future__ import annotations

from functools import lru_cache
from typing import Sequence

from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised application settings loaded from the environment."""

    APP_NAME: str = "SmartLocker Platform API"
    DEBUG: bool = False
    API_PREFIX: str = "/api"

    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@db:5432/smartlocker"
    REDIS_URL: RedisDsn = "redis://redis:6379/0"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    JWT_SECRET_KEY: str = "change-me"
    JWT_REFRESH_SECRET_KEY: str = "change-me-refresh"
    JWT_ALGORITHM: str = "HS256"

    S3_ENDPOINT_URL: str = "http://minio:9000"
    S3_ACCESS_KEY: str = "minio"
    S3_SECRET_KEY: str = "minio123"
    S3_BUCKET: str = "smartlocker"

    CORS_ORIGINS: Sequence[AnyHttpUrl | str] = ["http://localhost:3000"]

    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    DEFAULT_UNLOCK_TIME_MS: int = 5000
    DEFAULT_DELAY_OPEN_SEC: int = 2
    DEFAULT_WAIT_PUSH_DOOR_SEC: int = 10

    MAP_PROVIDER: str = "maplibre"

    RATE_LIMIT_ATTEMPTS: int = 5

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | Sequence[str]) -> Sequence[str]:  # noqa: N805
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
