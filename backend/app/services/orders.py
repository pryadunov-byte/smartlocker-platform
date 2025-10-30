"""Business logic for orders."""
from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..core import security
from ..models.access_code import AccessCode
from ..models.device import Device
from ..models.locker_cell import LockerCell, LockerCellStatus
from ..models.order import Order, OrderStatus, OrderType
from ..models.scenario import Scenario


class OrdersService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, *, status: OrderStatus | None = None) -> Iterable[Order]:
        query = (
            select(Order)
            .options(
                selectinload(Order.device),
                selectinload(Order.cell),
                selectinload(Order.access_code),
                selectinload(Order.notifications),
            )
            .order_by(Order.created_at.desc())
        )
        if status:
            query = query.where(Order.status == status)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get(self, order_id: int) -> Optional[Order]:
        result = await self.session.execute(
            select(Order)
                .options(
                    selectinload(Order.device),
                    selectinload(Order.cell),
                    selectinload(Order.access_code),
                )
                .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_by_public_uid(self, public_uid: str) -> Optional[Order]:
        result = await self.session.execute(
            select(Order)
                .options(
                    selectinload(Order.device),
                    selectinload(Order.cell),
                    selectinload(Order.access_code),
                )
                .where(Order.public_uid == public_uid)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        device: Device,
        cell: LockerCell | None,
        order_type: OrderType,
        scenario: Scenario | None,
        expires_at: datetime | None,
        payload: dict | None,
    ) -> Order:
        if not expires_at and scenario:
            params = scenario.params_json or {}
            storage_hours = int(params.get("storage_hours", 48))
            expires_at = datetime.utcnow() + timedelta(hours=storage_hours)

        base_payload = (payload or {}).copy()

        order = Order(
            public_uid=secrets.token_urlsafe(8),
            device=device,
            cell=cell,
            type=order_type,
            scenario=scenario,
            expires_at=expires_at,
            payload=base_payload,
        )
        self.session.add(order)
        await self.session.flush()

        pin = secrets.token_hex(3)
        access_code = AccessCode(order=order, pin_hash=security.hash_password(pin), qr_token=secrets.token_urlsafe(16))
        self.session.add(access_code)
        order.payload["pin_mask"] = f"{pin[:2]}**"
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def update_status(self, order: Order, *, status: OrderStatus) -> Order:
        order.status = status
        if status == OrderStatus.PICKED_UP:
            order.picked_up_at = datetime.utcnow()
        elif status == OrderStatus.OVERDUE and not order.expires_at:
            order.expires_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def mask_pin(self, order: Order) -> str:
        if order.payload and "pin_mask" in order.payload:
            return str(order.payload["pin_mask"])
        return "****"

    async def occupancy_percent(self) -> float:
        total = await self.session.execute(select(func.count(LockerCell.id)))
        occupied = await self.session.execute(
            select(func.count(LockerCell.id)).where(
                LockerCell.status.in_([LockerCellStatus.OCCUPIED, LockerCellStatus.OPEN])
            )
        )
        total_value = total.scalar() or 1
        return (occupied.scalar() or 0) / total_value * 100
