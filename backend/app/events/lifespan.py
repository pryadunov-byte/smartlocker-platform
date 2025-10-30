"""Application lifespan events."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ..core.logging import configure_logging
from ..db.session import engine

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    LOGGER.info("Starting SmartLocker API")
    try:
        yield
    finally:
        await engine.dispose()
        LOGGER.info("Shutdown SmartLocker API")
