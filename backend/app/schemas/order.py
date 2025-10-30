"""Order schemas for API interactions."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from ..models.order import OrderStatus, OrderType


class AccessCodeOut(BaseModel):
    attempts_left: int
    code_masked: str
    qr_token: str


class OrderBase(BaseModel):
    id: int
    public_uid: str
    device_id: int
    cell_id: Optional[int]
    type: OrderType
    status: OrderStatus
    created_at: datetime
    expires_at: Optional[datetime]
    picked_up_at: Optional[datetime]
    returned_at: Optional[datetime]


class OrderDetail(OrderBase):
    scenario_id: Optional[int]
    access_code: Optional[AccessCodeOut]
    payload: Optional[dict]


class OrderCreate(BaseModel):
    device_id: int
    cell_id: Optional[int]
    type: OrderType
    scenario_id: Optional[int]
    expires_at: Optional[datetime]
    payload: dict | None = Field(default_factory=dict)


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus]
    expires_at: Optional[datetime]
    picked_up_at: Optional[datetime]
    returned_at: Optional[datetime]
    payload: Optional[dict]
