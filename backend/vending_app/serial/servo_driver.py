from __future__ import annotations

import json
import logging
import time
from typing import List, Optional

from serial import SerialException

from serial.base_driver import BaseSerialDriver


class ServoDriver(BaseSerialDriver):
    def __init__(self, baudrate: int, preferred_ports: List[str], sector_count: int, home_angle: int = 0):
        super().__init__(baudrate=baudrate, preferred_ports=preferred_ports)
        self.sector_count = sector_count
        self.home_angle = home_angle
        self.current_angle: float = float(home_angle)
        self.logger = logging.getLogger("ServoDriver")

    def _send_command(self, command: str, payload: Optional[dict] = None, read_size: int = 16) -> bytes:
        packet = json.dumps({"cmd": command, "data": payload or {}}).encode("utf-8") + b"\n"
        self.logger.debug("Servo TX %s", packet)
        try:
            response = self.transact(packet, read_size=read_size)
            self.logger.debug("Servo RX %s", response)
            return response
        except SerialException as exc:
            self.logger.error("Servo serial error: %s", exc)
            self.close()
            raise

    def home(self) -> None:
        self._send_command("home")
        self.current_angle = float(self.home_angle)

    def rotate_to_sector(self, sector: int) -> float:
        angle = (360.0 / self.sector_count) * sector
        self.rotate_to_angle(angle)
        return angle

    def rotate_to_angle(self, angle: float) -> None:
        angle = max(0.0, min(360.0, angle))
        self._send_command("goto", {"angle": angle})
        self.current_angle = angle

    def rotate_relative(self, delta: float, smooth: bool = False) -> None:
        target = (self.current_angle + delta) % 360
        self._send_command("move", {"delta": delta, "smooth": smooth})
        self.current_angle = target

    def query_angle(self) -> float:
        response = self._send_command("angle", read_size=64)
        try:
            data = json.loads(response.decode("utf-8") or "{}")
            self.current_angle = float(data.get("angle", self.current_angle))
        except (json.JSONDecodeError, ValueError):
            self.logger.warning("Invalid servo response")
        return self.current_angle

    def request_error(self) -> Optional[str]:
        response = self._send_command("error", read_size=64)
        try:
            data = json.loads(response.decode("utf-8") or "{}")
            return data.get("error")
        except json.JSONDecodeError:
            return None

    def stop(self) -> None:
        self._send_command("stop")

    def await_motion_complete(self, timeout: float = 10.0) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            response = self._send_command("status", read_size=64)
            try:
                data = json.loads(response.decode("utf-8") or "{}")
                if data.get("status") == "idle":
                    return True
            except json.JSONDecodeError:
                pass
            time.sleep(0.2)
        return False
