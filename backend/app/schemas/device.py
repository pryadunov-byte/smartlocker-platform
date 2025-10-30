"""Device API schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ..models.alert import AlertKind, AlertSeverity
from ..models.locker_cell import LockerCellStatus


class LockerCellBase(BaseModel):
    id: int
    code: str
    size: str
    status: LockerCellStatus
    cooled: bool
    needs_repair: bool
    open: bool
    services_enabled: list[str] = Field(default_factory=list)


class DeviceBase(BaseModel):
    id: int
    code: str
    name: str
    geo_lat: Optional[float]
    geo_lon: Optional[float]
    status_online: bool
    firmware: Optional[str]
    last_seen_at: Optional[datetime]
    addr: int
    baud: int
    max_boards: int
    extra: Optional[dict]


class AlertOut(BaseModel):
    id: int
    severity: AlertSeverity
    kind: AlertKind
    message: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]


class DeviceDetail(DeviceBase):
    cells: list[LockerCellBase]
    alerts: list[AlertOut]


class DeviceUpdate(BaseModel):
    name: Optional[str]
    firmware: Optional[str]
    status_online: Optional[bool]
    max_boards: Optional[int]


class LockerCellUpdate(BaseModel):
    status: Optional[LockerCellStatus]
    cooled: Optional[bool]
    needs_repair: Optional[bool]
    services_enabled: Optional[list[str]]
