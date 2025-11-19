from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from typing import Callable, Optional

import serial
from serial.serialutil import SerialException
from serial.tools import list_ports


@dataclass
class PortInfo:
    name: str
    description: str


class BaseSerialDriver:
    def __init__(self, baudrate: int, preferred_ports: list[str], timeout: float = 0.2):
        self.baudrate = baudrate
        self.preferred_ports = preferred_ports
        self.timeout = timeout
        self._lock = threading.Lock()
        self._serial: Optional[serial.Serial] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def list_candidate_ports(self) -> list[PortInfo]:
        ports = [PortInfo(p.device, p.description) for p in list_ports.comports()]
        ports.sort(key=lambda p: (0 if p.name in self.preferred_ports else 1, p.name))
        return ports

    def connect(self, port: str) -> bool:
        try:
            self._serial = serial.Serial(port=port, baudrate=self.baudrate, timeout=self.timeout)
            self.logger.info("Connected to %s", port)
            return True
        except SerialException as exc:
            self.logger.error("Failed to open %s: %s", port, exc)
            self._serial = None
            return False

    def auto_connect(self) -> bool:
        for port in self.list_candidate_ports():
            if self.connect(port.name):
                return True
        self.logger.warning("No serial ports available for %s", self.__class__.__name__)
        return False

    def close(self) -> None:
        with self._lock:
            if self._serial and self._serial.is_open:
                self.logger.info("Closing serial port %s", self._serial.port)
                self._serial.close()
            self._serial = None

    def is_connected(self) -> bool:
        return bool(self._serial and self._serial.is_open)

    def write(self, payload: bytes) -> None:
        if not self.is_connected():
            raise SerialException("Driver is not connected")
        with self._lock:
            self._serial.write(payload)

    def read(self, size: int = 1) -> bytes:
        if not self.is_connected():
            raise SerialException("Driver is not connected")
        with self._lock:
            return self._serial.read(size)

    def transact(self, payload: bytes, response_handler: Callable[[bytes], None] | None = None, read_size: int = 32) -> bytes:
        self.write(payload)
        data = self.read(read_size)
        if response_handler:
            response_handler(data)
        return data

    def reconnect(self) -> bool:
        if self.is_connected():
            return True
        return self.auto_connect()
