from __future__ import annotations

import logging
import threading
import time
from typing import Callable, List


class Watchdog(threading.Thread):
    def __init__(self, interval: int, actions: List[Callable[[], bool]], name: str = "watchdog"):
        super().__init__(daemon=True)
        self.interval = interval
        self.actions = actions
        self._stop_event = threading.Event()
        self.logger = logging.getLogger(name)

    def run(self) -> None:
        while not self._stop_event.is_set():
            for action in self.actions:
                try:
                    result = action()
                    self.logger.debug("Watchdog action %s -> %s", action, result)
                except Exception as exc:  # noqa: BLE001
                    self.logger.error("Watchdog action error: %s", exc)
            time.sleep(self.interval)

    def stop(self) -> None:
        self._stop_event.set()
