from __future__ import annotations

import logging
import struct
from typing import List, Optional

from serial import SerialException

from serial.base_driver import BaseSerialDriver

STX = 0x02
ETX = 0x03


class CU24Driver(BaseSerialDriver):
    def __init__(self, baudrate: int, preferred_ports: List[str], address: int):
        super().__init__(baudrate=baudrate, preferred_ports=preferred_ports)
        self.address = address
        self.logger = logging.getLogger("CU24Driver")

    @staticmethod
    def checksum(payload: bytes) -> int:
        return sum(payload) & 0xFF

    def _packet(self, locknum: int, cmd: int, ask: int = 0x00, data: bytes | None = None) -> bytes:
        data = data or b""
        frame = bytearray([STX, self.address & 0xFF, locknum & 0xFF, cmd & 0xFF, ask & 0xFF, len(data), ETX])
        frame.extend(data)
        frame.append(self.checksum(frame[1:]))
        return bytes(frame)

    def _transact(self, locknum: int, cmd: int, ask: int = 0x00, data: bytes | None = None, read_size: int = 16) -> bytes:
        packet = self._packet(locknum, cmd, ask, data)
        self.logger.debug("TX %s", packet.hex())
        try:
            response = self.transact(packet, read_size=read_size)
            self.logger.debug("RX %s", response.hex())
            return response
        except SerialException as exc:
            self.logger.error("Serial error: %s", exc)
            self.close()
            raise

    def get_status(self, locknum: int = 0x64) -> bytes:
        return self._transact(locknum, 0x80, read_size=16)

    def unlock(self, locknum: int) -> None:
        self._transact(locknum, 0x81, read_size=8)

    def query_unlock_time(self) -> Optional[int]:
        response = self._transact(0x00, 0x82, read_size=10)
        if len(response) >= 10:
            value = struct.unpack(">H", response[7:9])[0]
            return value * 10
        return None

    def set_unlock_time(self, value_ms: int) -> None:
        payload = struct.pack(">H", max(0, min(6000, value_ms // 10)))
        self._transact(0x00, 0x82, data=payload, read_size=8)

    def set_baudrate(self, mode: int) -> None:
        self._transact(0x00, 0x83, data=bytes([mode & 0x03]), read_size=8)

    def set_delayed_unlock(self, seconds: int) -> None:
        payload = bytes([max(0, min(200, seconds))])
        self._transact(0x00, 0x84, data=payload)

    def set_push_door_time(self, seconds: int) -> None:
        payload = bytes([max(0, min(200, seconds))])
        self._transact(0x00, 0x85, data=payload)

    def initialize(self) -> None:
        self._transact(0x00, 0x8E)

    def get_version(self) -> bytes:
        return self._transact(0x00, 0x8F, read_size=16)

    def ensure_connection(self) -> bool:
        if not self.is_connected():
            return self.auto_connect()
        return True
