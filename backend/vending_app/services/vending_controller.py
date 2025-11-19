from __future__ import annotations

import datetime as dt
import logging
from dataclasses import dataclass
from typing import Optional

from config import AppConfig
from db.db_manager import DbManager
from serial.cu24_driver import CU24Driver
from serial.servo_driver import ServoDriver


@dataclass
class OperationResult:
    success: bool
    message: str
    row: int | None = None
    sector: int | None = None


class VendingController:
    def __init__(self, config: AppConfig, db: DbManager, lock_driver: CU24Driver, servo_driver: ServoDriver):
        self.config = config
        self.db = db
        self.lock_driver = lock_driver
        self.servo_driver = servo_driver
        self.logger = logging.getLogger("VendingController")
        self.rows = 15
        self.sectors = self.config.servo.sector_count
        self._restore_context()

    def _restore_context(self) -> None:
        state = self.db.get_state("servo")
        if state:
            self.servo_driver.current_angle = float(state.get("angle", 0))
        else:
            self.db.set_state("servo", {"angle": self.servo_driver.current_angle})

    def _persist_angle(self) -> None:
        self.db.set_state("servo", {"angle": self.servo_driver.current_angle})

    def _ensure_devices(self) -> bool:
        lock_ok = self.lock_driver.ensure_connection()
        servo_ok = self.servo_driver.reconnect()
        return lock_ok and servo_ok

    def _log_and_save(
        self,
        fio: str,
        barcode: str,
        item: str,
        row: int,
        sector: int,
        action_type: str,
    ) -> None:
        timestamp = dt.datetime.now().isoformat(sep=" ", timespec="seconds")
        self.db.log_transaction(fio, barcode, item, row, sector, action_type, timestamp)
        if action_type == "load":
            self.db.set_inventory(barcode, fio, item, row, sector, timestamp)
        else:
            self.db.remove_inventory(barcode)

    def load_item(self, fio: str, barcode: str, item: str, row: int, sector: int) -> OperationResult:
        if not self._ensure_devices():
            return OperationResult(False, "Нет подключения к оборудованию")
        try:
            self.servo_driver.rotate_to_sector(sector)
            self.servo_driver.await_motion_complete()
            lock_number = self._lock_number(row)
            self.lock_driver.unlock(lock_number)
            self._persist_angle()
            self._log_and_save(fio, barcode, item, row, sector, "load")
            return OperationResult(True, "Загрузка завершена", row, sector)
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Ошибка загрузки")
            return OperationResult(False, str(exc))

    def issue_item(self, fio: str, barcode: str, item: str) -> OperationResult:
        record = self.db.get_inventory(barcode)
        if not record:
            return OperationResult(False, "Предмет не найден в базе")
        row = int(record["row_no"])
        sector = int(record["sector"])
        if not self._ensure_devices():
            return OperationResult(False, "Нет подключения к оборудованию")
        try:
            self.servo_driver.rotate_to_sector(sector)
            self.servo_driver.await_motion_complete()
            lock_number = self._lock_number(row)
            self.lock_driver.unlock(lock_number)
            self._persist_angle()
            self._log_and_save(fio, barcode, item or record["item"], row, sector, "issue")
            return OperationResult(True, "Выдача завершена", row, sector)
        except Exception as exc:  # noqa: BLE001
            self.logger.exception("Ошибка выдачи")
            return OperationResult(False, str(exc))

    def _lock_number(self, row: int) -> int:
        return max(0, min(23, row - 1))

    def status(self) -> dict:
        return {
            "lock_connected": self.lock_driver.is_connected(),
            "servo_connected": self.servo_driver.is_connected(),
            "angle": self.servo_driver.current_angle,
        }
