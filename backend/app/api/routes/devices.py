"""Device management endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.device import DeviceDetail, DeviceUpdate, LockerCellUpdate
from ...services.devices import DevicesService
from ..deps import get_db_session, require_roles

router = APIRouter(dependencies=[Depends(require_roles())])


@router.get("/", response_model=list[DeviceDetail])
async def list_devices(session: AsyncSession = Depends(get_db_session)):
    service = DevicesService(session)
    devices = await service.list()
    output: list[DeviceDetail] = []
    for device in devices:
        output.append(
            DeviceDetail(
                id=device.id,
                code=device.code,
                name=device.name,
                geo_lat=device.geo_lat,
                geo_lon=device.geo_lon,
                status_online=device.status_online,
                firmware=device.firmware,
                last_seen_at=device.last_seen_at,
                addr=device.addr,
                baud=device.baud,
                max_boards=device.max_boards,
                extra=device.extra,
                cells=[
                    {
                        "id": cell.id,
                        "code": cell.code,
                        "size": cell.size,
                        "status": cell.status,
                        "cooled": cell.cooled,
                        "needs_repair": cell.needs_repair,
                        "open": cell.open,
                        "services_enabled": cell.services_enabled,
                    }
                    for cell in device.cells
                ],
                alerts=[
                    {
                        "id": alert.id,
                        "severity": alert.severity,
                        "kind": alert.kind,
                        "message": alert.message,
                        "created_at": alert.created_at,
                        "resolved_at": alert.resolved_at,
                    }
                    for alert in device.alerts
                ],
            )
        )
    return output


@router.patch("/{device_id}", response_model=DeviceDetail)
async def update_device(device_id: int, payload: DeviceUpdate, session: AsyncSession = Depends(get_db_session)):
    service = DevicesService(session)
    device = await service.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device = await service.update(device, payload.dict(exclude_unset=True))
    return await _serialize_device(device)


@router.patch("/cells/{cell_id}")
async def update_cell(cell_id: int, payload: LockerCellUpdate, session: AsyncSession = Depends(get_db_session)):
    service = DevicesService(session)
    cell = await service.get_cell(cell_id)
    if not cell:
        raise HTTPException(status_code=404, detail="Cell not found")
    await service.update_cell(cell, payload.dict(exclude_unset=True))
    return {"status": "updated"}


async def _serialize_device(device) -> DeviceDetail:
    return DeviceDetail(
        id=device.id,
        code=device.code,
        name=device.name,
        geo_lat=device.geo_lat,
        geo_lon=device.geo_lon,
        status_online=device.status_online,
        firmware=device.firmware,
        last_seen_at=device.last_seen_at,
        addr=device.addr,
        baud=device.baud,
        max_boards=device.max_boards,
        extra=device.extra,
        cells=[
            {
                "id": cell.id,
                "code": cell.code,
                "size": cell.size,
                "status": cell.status,
                "cooled": cell.cooled,
                "needs_repair": cell.needs_repair,
                "open": cell.open,
                "services_enabled": cell.services_enabled,
            }
            for cell in device.cells
        ],
        alerts=[
            {
                "id": alert.id,
                "severity": alert.severity,
                "kind": alert.kind,
                "message": alert.message,
                "created_at": alert.created_at,
                "resolved_at": alert.resolved_at,
            }
            for alert in device.alerts
        ],
    )
