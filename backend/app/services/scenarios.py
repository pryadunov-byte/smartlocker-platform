"""Scenario service."""
from __future__ import annotations

from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.scenario import Scenario


class ScenarioService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> Iterable[Scenario]:
        result = await self.session.execute(select(Scenario))
        return result.scalars().all()

    async def get(self, scenario_id: int) -> Optional[Scenario]:
        result = await self.session.execute(select(Scenario).where(Scenario.id == scenario_id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Scenario]:
        result = await self.session.execute(select(Scenario).where(Scenario.name == name))
        return result.scalar_one_or_none()

    async def create(self, name: str, params: dict) -> Scenario:
        existing = await self.get_by_name(name)
        if existing:
            return existing
        scenario = Scenario(name=name, params_json=params)
        self.session.add(scenario)
        await self.session.commit()
        await self.session.refresh(scenario)
        return scenario

    async def update(self, scenario: Scenario, *, name: str | None = None, params: dict | None = None) -> Scenario:
        if name:
            scenario.name = name
        if params is not None:
            scenario.params_json = params
        await self.session.commit()
        await self.session.refresh(scenario)
        return scenario
