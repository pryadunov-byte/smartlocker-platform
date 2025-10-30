"""Schemas for public mobile web service."""
from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import BaseModel


class PublicOrder(BaseModel):
    public_uid: str
    device_name: str
    device_address: str | None
    created_at: datetime
    expires_at: datetime
    expires_in: timedelta
    code_masked: str
    qr_svg: str
    map_point: dict[str, float]


class PaymentResponse(BaseModel):
    status: str


class SupportRequest(BaseModel):
    order_public_uid: str
    issue: str
    contact: str | None = None


class SupportResponse(BaseModel):
    ticket_id: str
