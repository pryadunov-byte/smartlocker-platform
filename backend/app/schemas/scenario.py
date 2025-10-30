"""Scenario configuration schemas."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ScenarioParams(BaseModel):
    storage_hours: int = Field(default=48, ge=1)
    tariff_cents: int = Field(default=0, ge=0)
    penalty_cents: int = Field(default=0, ge=0)
    escalation_channels: list[str] = Field(default_factory=list)
    unlock_time_ms: int = Field(default=5000, ge=0)
    delay_open_sec: int = Field(default=0, ge=0)
    wait_push_door_sec: int = Field(default=0, ge=0)


class ScenarioBase(BaseModel):
    id: int
    name: str
    params_json: ScenarioParams


class ScenarioCreate(BaseModel):
    name: str
    params_json: ScenarioParams


class ScenarioUpdate(BaseModel):
    name: str | None = None
    params_json: ScenarioParams | None = None
