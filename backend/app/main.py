"""Application entrypoint for the SmartLocker platform API."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .events.lifespan import lifespan
from .api.routes import api_router


def create_app() -> FastAPI:
    """Instantiate the FastAPI application with middleware and routers."""
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app


app = create_app()


@api_router.get("/health", tags=["health"], include_in_schema=False)
async def health() -> dict[str, str]:
    """Basic readiness probe used by Docker health checks."""
    return {"status": "ok"}
