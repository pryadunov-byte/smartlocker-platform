"""Shared Pydantic schemas."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ORMModel(BaseModel):
    class Config:
        orm_mode = True


class TimeStampedModel(ORMModel):
    created_at: datetime
