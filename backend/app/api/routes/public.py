"""Public mobile web service endpoints."""
from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.public import PaymentResponse, PublicOrder, SupportRequest, SupportResponse
from ...services.orders import OrdersService
from ..deps import get_db_session

router = APIRouter()


@router.get("/orders/{public_uid}", response_model=PublicOrder)
async def get_public_order(public_uid: str, session: AsyncSession = Depends(get_db_session)):
    service = OrdersService(session)
    order = await service.get_by_public_uid(public_uid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not order.access_code:
        raise HTTPException(status_code=400, detail="Access code missing")
    now = datetime.utcnow()
    expires_at = order.expires_at or now
    expires_in = expires_at - now
    if expires_in.total_seconds() < 0:
        expires_in = timedelta(seconds=0)

    return PublicOrder(
        public_uid=order.public_uid,
        device_name=order.device.name if order.device else "",
        device_address=order.device.extra.get("address") if order.device and order.device.extra else None,
        created_at=order.created_at,
        expires_at=expires_at,
        expires_in=expires_in,
        code_masked=await service.mask_pin(order),
        qr_svg=f"QR({order.access_code.qr_token})",
        map_point={"lat": order.device.geo_lat or 0.0, "lon": order.device.geo_lon or 0.0},
    )


@router.post("/orders/{public_uid}/pay", response_model=PaymentResponse)
async def pay_order(public_uid: str):
    return PaymentResponse(status="paid")


@router.post("/support", response_model=SupportResponse)
async def support(payload: SupportRequest) -> SupportResponse:
    return SupportResponse(ticket_id=f"SUP-{payload.order_public_uid}")
