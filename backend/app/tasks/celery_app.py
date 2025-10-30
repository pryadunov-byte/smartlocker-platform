"""Celery application for background tasks."""
from __future__ import annotations

from celery import Celery

from ..core.config import settings

celery_app = Celery(
    "smartlocker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.autodiscover_tasks(["app.tasks"])
