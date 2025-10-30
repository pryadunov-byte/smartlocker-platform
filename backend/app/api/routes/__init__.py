"""Top level API router that assembles all versioned endpoints."""
from fastapi import APIRouter

from .auth import router as auth_router
from .orders import router as orders_router
from .devices import router as devices_router
from .scenarios import router as scenarios_router
from .notifications import router as notifications_router
from .public import router as public_router
from .device_portal import router as device_router
from .analytics import router as analytics_router
from .alerts import router as alerts_router
from .users import router as users_router
from .websocket import router as websocket_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(devices_router, prefix="/devices", tags=["devices"])
api_router.include_router(scenarios_router, prefix="/scenarios", tags=["scenarios"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
api_router.include_router(public_router, prefix="/public", tags=["public"], include_in_schema=False)
api_router.include_router(device_router, prefix="/device", tags=["device"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(websocket_router, prefix="/ws", tags=["websocket"])
