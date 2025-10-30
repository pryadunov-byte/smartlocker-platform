"""Celery tasks for notification delivery."""
from __future__ import annotations

import logging

from .celery_app import celery_app

LOGGER = logging.getLogger(__name__)


@celery_app.task(name="notifications.send")
def send_notification(notification_id: int) -> None:
    LOGGER.info("Sending notification %s", notification_id)
