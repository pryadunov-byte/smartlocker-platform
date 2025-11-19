import json
from pathlib import Path
from dataclasses import dataclass
from typing import List

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


@dataclass
class KerongConfig:
    baudrate: int
    address: int
    preferred_ports: List[str]
    unlock_time_ms: int


@dataclass
class ServoConfig:
    baudrate: int
    preferred_ports: List[str]
    home_angle: int
    sector_count: int


@dataclass
class WatchdogConfig:
    interval_seconds: int
    retry_limit: int


@dataclass
class UIConfig:
    theme: str


@dataclass
class AppConfig:
    app_name: str
    database_path: Path
    log_level: str
    kerong: KerongConfig
    servo: ServoConfig
    watchdog: WatchdogConfig
    ui: UIConfig


def load_config(path: Path | None = None) -> AppConfig:
    target = path or CONFIG_PATH
    with target.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return AppConfig(
        app_name=raw.get("appName", "SmartLocker"),
        database_path=(target.parent / raw.get("databasePath", "db/database.sqlite")).resolve(),
        log_level=raw.get("logLevel", "INFO"),
        kerong=KerongConfig(
            baudrate=raw["kerong"].get("baudrate", 19200),
            address=raw["kerong"].get("address", 1),
            preferred_ports=raw["kerong"].get("preferredPorts", []),
            unlock_time_ms=raw["kerong"].get("unlockTimeMs", 500),
        ),
        servo=ServoConfig(
            baudrate=raw["servo"].get("baudrate", 115200),
            preferred_ports=raw["servo"].get("preferredPorts", []),
            home_angle=raw["servo"].get("homeAngle", 0),
            sector_count=raw["servo"].get("sectorCount", 32),
        ),
        watchdog=WatchdogConfig(
            interval_seconds=raw["watchdog"].get("intervalSeconds", 10),
            retry_limit=raw["watchdog"].get("retryLimit", 3),
        ),
        ui=UIConfig(theme=raw.get("ui", {}).get("theme", "dark")),
    )
