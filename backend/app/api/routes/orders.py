"""Order endpoints for back-office."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.locker_cell import LockerCell
from ...models.order import OrderStatus, OrderType
from ...schemas.order import AccessCodeOut, OrderCreate, OrderDetail, OrderUpdate
from ...services.devices import DevicesService
from ...services.orders import OrdersService
from ...services.scenarios import ScenarioService
from ..deps import get_db_session, require_roles

router = APIRouter(dependencies=[Depends(require_roles())])


@router.get("/", response_model=list[OrderDetail])
async def list_orders(
    session: AsyncSession = Depends(get_db_session),
    status: OrderStatus | None = Query(default=None),
):
    service = OrdersService(session)
    orders = await service.list(status=status)
    output: list[OrderDetail] = []
    for order in orders:
        code_masked = await service.mask_pin(order)
        output.append(
            OrderDetail(
                id=order.id,
                public_uid=order.public_uid,
                device_id=order.device_id,
                cell_id=order.cell_id,
                type=order.type,
                status=order.status,
                created_at=order.created_at,
                expires_at=order.expires_at,
                picked_up_at=order.picked_up_at,
                returned_at=order.returned_at,
                scenario_id=order.scenario_id,
                payload=order.payload,
                access_code=
                AccessCodeOut(
                    attempts_left=order.access_code.attempts_left,
                    code_masked=code_masked,
                    qr_token=order.access_code.qr_token,
                )
                if order.access_code
                else None,
            )
        )
    return output


@router.post("/", response_model=OrderDetail, status_code=201)
async def create_order(payload: OrderCreate, session: AsyncSession = Depends(get_db_session)):
    device_service = DevicesService(session)
    scenario_service = ScenarioService(session)
    orders_service = OrdersService(session)

    device = await device_service.get(payload.device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    cell: LockerCell | None = None
    if payload.cell_id:
        cell = await device_service.get_cell(payload.cell_id)
        if not cell:
            raise HTTPException(status_code=404, detail="Cell not found")

    scenario = None
    if payload.scenario_id:
        scenario = await scenario_service.get(payload.scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")

    order = await orders_service.create(
        device=device,
        cell=cell,
        order_type=payload.type,
        scenario=scenario,
        expires_at=payload.expires_at,
        payload=payload.payload,
    )
    code_masked = await orders_service.mask_pin(order)
    return OrderDetail(
        id=order.id,
        public_uid=order.public_uid,
        device_id=order.device_id,
        cell_id=order.cell_id,
        type=order.type,
        status=order.status,
        created_at=order.created_at,
        expires_at=order.expires_at,
        picked_up_at=order.picked_up_at,
        returned_at=order.returned_at,
        scenario_id=order.scenario_id,
        payload=order.payload,
        access_code=
        AccessCodeOut(
            attempts_left=order.access_code.attempts_left,
            code_masked=code_masked,
            qr_token=order.access_code.qr_token,
        )
        if order.access_code
        else None,
    )


@router.patch("/{order_id}", response_model=OrderDetail)
async def update_order(order_id: int, payload: OrderUpdate, session: AsyncSession = Depends(get_db_session)):
    service = OrdersService(session)
    order = await service.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = payload.dict(exclude_unset=True)
    if "status" in update_data:
        order = await service.update_status(order, status=update_data.pop("status"))

    for field, value in update_data.items():
        setattr(order, field, value)
    await session.commit()
    await session.refresh(order)
    code_masked = await service.mask_pin(order)
    return OrderDetail(
        id=order.id,
        public_uid=order.public_uid,
        device_id=order.device_id,
        cell_id=order.cell_id,
        type=order.type,
        status=order.status,
        created_at=order.created_at,
        expires_at=order.expires_at,
        picked_up_at=order.picked_up_at,
        returned_at=order.returned_at,
        scenario_id=order.scenario_id,
        payload=order.payload,
        access_code=
        AccessCodeOut(
            attempts_left=order.access_code.attempts_left,
            code_masked=code_masked,
            qr_token=order.access_code.qr_token,
        )
        if order.access_code
        else None,
    )
