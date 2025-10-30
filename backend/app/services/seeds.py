"""Seed data utility."""
from __future__ import annotations

import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.device import Device
from ..models.locker_cell import LockerCell, LockerCellStatus
from ..models.order import OrderStatus, OrderType
from ..models.user import UserRole
from .orders import OrdersService
from .scenarios import ScenarioService
from .users import UsersService

CITIES = [
    ("Moscow", 55.751244, 37.618423),
    ("St. Petersburg", 59.93428, 30.335099),
    ("Novosibirsk", 55.008353, 82.935733),
    ("Kazan", 55.830433, 49.066082),
    ("Yekaterinburg", 56.838926, 60.605703),
]


async def seed_demo(session: AsyncSession) -> None:
    user_service = UsersService(session)
    for email, role, password in [
        ("admin@demo.local", UserRole.ADMIN, "Admin123!"),
        ("operator@demo.local", UserRole.OPERATOR, "Operator123!"),
        ("technician@demo.local", UserRole.TECHNICIAN, "Tech123!"),
    ]:
        if not await user_service.get_by_email(email):
            await user_service.create(email, password, role)

    devices: list[Device] = []
    for idx in range(10):
        city, lat, lon = random.choice(CITIES)
        device = Device(
            code=f"DEV-{idx:03d}",
            name=f"Locker {city} #{idx}",
            geo_lat=lat + random.uniform(-0.05, 0.05),
            geo_lon=lon + random.uniform(-0.05, 0.05),
            status_online=True,
            firmware="1.0.0",
            addr=idx,
            baud=19200,
            extra={"address": f"{city}, ул. Демонстрационная, д. {idx + 10}"},
        )
        session.add(device)
        devices.append(device)
    await session.flush()

    for device in devices:
        for slot in range(30):
            cell = LockerCell(
                device_id=device.id,
                code=f"{chr(65 + slot // 10)}{slot % 10}",
                size=random.choice(["S", "M", "L"]),
                status=random.choice(list(LockerCellStatus)),
                cooled=random.choice([True, False]),
                needs_repair=False,
                open=False,
                services_enabled=["delivery", "return"],
            )
            session.add(cell)
    await session.flush()

    scenario_service = ScenarioService(session)
    default_scenario = await scenario_service.create(
        "Standard Delivery",
        {
            "storage_hours": 72,
            "tariff_cents": 1500,
            "penalty_cents": 500,
            "escalation_channels": ["sms", "email"],
            "unlock_time_ms": 5000,
            "delay_open_sec": 2,
            "wait_push_door_sec": 15,
        },
    )

    orders_service = OrdersService(session)
    for idx in range(120):
        device = random.choice(devices)
        cell = random.choice(device.cells)
        order = await orders_service.create(
            device=device,
            cell=cell,
            order_type=random.choice(list(OrderType)),
            scenario=default_scenario,
            expires_at=datetime.utcnow() + timedelta(hours=48),
            payload={"city": device.name},
        )
        order.status = random.choice(list(OrderStatus))
    await session.commit()
