from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import load_config
from db.db_manager import DbManager
from gui.main_window import MainWindow
from serial.cu24_driver import CU24Driver
from serial.servo_driver import ServoDriver
from services.vending_controller import VendingController
from services.watchdog import Watchdog


def setup_logging(log_dir: Path, level: str) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "app.log"
    device_log_path = log_dir / "device.log"
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    device_handler = logging.FileHandler(device_log_path, encoding="utf-8")
    device_handler.setFormatter(formatter)
    device_handler.setLevel(logging.DEBUG)
    logging.getLogger("CU24Driver").addHandler(device_handler)
    logging.getLogger("ServoDriver").addHandler(device_handler)


def main() -> int:
    base_path = Path(__file__).resolve().parent
    config = load_config(base_path / "config.json")
    setup_logging(base_path / "logs", config.log_level)

    db = DbManager(config.database_path)
    lock_driver = CU24Driver(config.kerong.baudrate, config.kerong.preferred_ports, config.kerong.address)
    servo_driver = ServoDriver(
        config.servo.baudrate,
        config.servo.preferred_ports,
        config.servo.sector_count,
        config.servo.home_angle,
    )

    controller = VendingController(config, db, lock_driver, servo_driver)

    watchdog = Watchdog(
        interval=config.watchdog.interval_seconds,
        actions=[lock_driver.reconnect, servo_driver.reconnect],
        name="device-watchdog",
    )
    watchdog.start()

    app = QApplication(sys.argv)
    window = MainWindow(controller, db)
    window.show()
    exit_code = app.exec()

    watchdog.stop()
    db.close()
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
