"""Analytics DTOs."""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class OccupancyDataPoint(BaseModel):
    date: date
    occupancy_percent: float


class RomiDataPoint(BaseModel):
    channel: str
    spend: float
    revenue: float


class AnalyticsDashboard(BaseModel):
    devices_online: int
    devices_offline: int
    active_orders: int
    overdue_orders: int
    average_storage_time_hours: float
    occupancy_series: list[OccupancyDataPoint]
    romi: list[RomiDataPoint]
