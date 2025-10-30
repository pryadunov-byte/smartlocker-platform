"""Device service for inventory and monitoring."""
from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.device import Device
from ..models.locker_cell import LockerCell


class DevicesService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> Iterable[Device]:
        result = await self.session.execute(
            select(Device).options(selectinload(Device.cells), selectinload(Device.alerts))
        )
        return result.scalars().all()

    async def get(self, device_id: int) -> Optional[Device]:
        result = await self.session.execute(
            select(Device)
            .options(selectinload(Device.cells), selectinload(Device.alerts))
            .where(Device.id == device_id)
        )
        return result.scalar_one_or_none()

    async def update(self, device: Device, data: dict) -> Device:
        for key, value in data.items():
            setattr(device, key, value)
        await self.session.commit()
        await self.session.refresh(device)
        return device

    async def update_cell(self, cell: LockerCell, data: dict) -> LockerCell:
        for key, value in data.items():
            setattr(cell, key, value)
        await self.session.commit()
        await self.session.refresh(cell)
        return cell

    async def get_cell(self, cell_id: int) -> Optional[LockerCell]:
        result = await self.session.execute(select(LockerCell).where(LockerCell.id == cell_id))
        return result.scalar_one_or_none()
