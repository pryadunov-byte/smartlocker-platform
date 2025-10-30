"""Scenario configuration endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.scenario import ScenarioBase, ScenarioCreate, ScenarioUpdate
from ...services.scenarios import ScenarioService
from ..deps import get_db_session, require_roles

router = APIRouter(dependencies=[Depends(require_roles())])


@router.get("/", response_model=list[ScenarioBase])
async def list_scenarios(session: AsyncSession = Depends(get_db_session)):
    service = ScenarioService(session)
    scenarios = await service.list()
    return [ScenarioBase(id=sc.id, name=sc.name, params_json=sc.params_json) for sc in scenarios]


@router.post("/", response_model=ScenarioBase, status_code=201)
async def create_scenario(payload: ScenarioCreate, session: AsyncSession = Depends(get_db_session)):
    service = ScenarioService(session)
    scenario = await service.create(payload.name, payload.params_json.dict())
    return ScenarioBase(id=scenario.id, name=scenario.name, params_json=scenario.params_json)


@router.patch("/{scenario_id}", response_model=ScenarioBase)
async def update_scenario(scenario_id: int, payload: ScenarioUpdate, session: AsyncSession = Depends(get_db_session)):
    service = ScenarioService(session)
    scenario = await service.get(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    scenario = await service.update(
        scenario,
        name=payload.name,
        params=payload.params_json.dict() if payload.params_json else None,
    )
    return ScenarioBase(id=scenario.id, name=scenario.name, params_json=scenario.params_json)
