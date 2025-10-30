"""Endpoints consumed by physical device controllers."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core import security
from ...models.device import Device
from ...schemas.device import DeviceDetail
from ...services.devices import DevicesService
from ...services.orders import OrdersService
from ..deps import get_db_session

router = APIRouter()


@router.post("/check-in")
async def device_check_in(payload: dict, session: AsyncSession = Depends(get_db_session)):
    service = DevicesService(session)
    device = await service.get(payload.get("deviceId"))
    if device:
        await service.update(device, {"last_seen_at": payload.get("timestamp"), "status_online": True})
    return {"status": "ok"}


@router.post("/open")
async def device_open(payload: dict, session: AsyncSession = Depends(get_db_session)):
    orders = OrdersService(session)
    token = payload.get("tokenOrPin", "")
    order = await orders.get_by_public_uid(token)
    if not order:
        # fallback to PIN validation across known orders
        for candidate in await orders.list():
            if candidate.access_code and security.verify_password(token, candidate.access_code.pin_hash):
                order = candidate
                break
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await orders.update_status(order, status=order.status)
    return {"result": "opened", "hookState": "unlocked", "openTimeMs": 1500}


@router.get("/{device_id}/status", response_model=DeviceDetail)
async def device_status(device_id: int, session: AsyncSession = Depends(get_db_session)):
    service = DevicesService(session)
    device = await service.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return await _serialize_device(device)


async def _serialize_device(device: Device) -> DeviceDetail:
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
