from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str = "SmartLocker API"
    DB_DSN: str = "postgresql+asyncpg://postgres:postgres@db:5432/smartlocker"
    REDIS_URL: str = "redis://redis:6379/0"
    class Config: env_file = ".env"
settings = Settings()
