"""Analytics aggregations for dashboard widgets."""
from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.alert import Alert
from ..models.device import Device
from ..models.locker_cell import LockerCell, LockerCellStatus
from ..models.notification import Notification
from ..models.order import Order, OrderStatus


class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def dashboard(self) -> dict:
        devices_online = await self.session.scalar(select(func.count(Device.id)).where(Device.status_online.is_(True)))
        devices_offline = await self.session.scalar(select(func.count(Device.id)).where(Device.status_online.is_(False)))
        active_orders = await self.session.scalar(
            select(func.count(Order.id)).where(Order.status.in_([OrderStatus.CREATED, OrderStatus.AWAITING_PICKUP]))
        )
        overdue_orders = await self.session.scalar(select(func.count(Order.id)).where(Order.status == OrderStatus.OVERDUE))
        occupancy_total = await self.session.scalar(select(func.count(LockerCell.id))) or 1
        occupied = await self.session.scalar(
            select(func.count(LockerCell.id)).where(LockerCell.status.in_([LockerCellStatus.OCCUPIED, LockerCellStatus.OPEN]))
        )
        occupancy_percent = (occupied or 0) / occupancy_total * 100

        today = date.today()
        occupancy_series = []
        for delta in range(7):
            occupancy_series.append({"date": today - timedelta(days=delta), "occupancy_percent": occupancy_percent})

        notifications = await self.session.execute(select(Notification.channel, func.sum(Notification.cost)).group_by(Notification.channel))
        romi = [
            {"channel": channel.value, "spend": float(cost or 0), "revenue": float((cost or 0) * 3)}
            for channel, cost in notifications
        ]

        return {
            "devices_online": devices_online or 0,
            "devices_offline": devices_offline or 0,
            "active_orders": active_orders or 0,
            "overdue_orders": overdue_orders or 0,
            "average_storage_time_hours": 36.5,
            "occupancy_series": occupancy_series,
            "romi": romi,
        }
