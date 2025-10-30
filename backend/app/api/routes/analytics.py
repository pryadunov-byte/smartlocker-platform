"""Analytics routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.analytics import AnalyticsDashboard
from ...services.analytics import AnalyticsService
from ..deps import get_db_session, require_roles

router = APIRouter(dependencies=[Depends(require_roles())])


@router.get("/dashboard", response_model=AnalyticsDashboard)
async def dashboard(session: AsyncSession = Depends(get_db_session)):
    service = AnalyticsService(session)
    data = await service.dashboard()
    return AnalyticsDashboard(**data)
