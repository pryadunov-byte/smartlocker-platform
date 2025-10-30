"""Alert API schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.alert import AlertKind, AlertSeverity


class AlertCreate(BaseModel):
    device_id: int
    severity: AlertSeverity
    kind: AlertKind
    message: Optional[str] = None


class AlertOut(BaseModel):
    id: int
    device_id: int
    severity: AlertSeverity
    kind: AlertKind
    message: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]
