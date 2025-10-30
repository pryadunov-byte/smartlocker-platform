"""KR-CU24 controller driver abstraction."""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Iterable

LOGGER = logging.getLogger(__name__)


@dataclass
class CommandResult:
    success: bool
    payload: bytes | None = None
    error: str | None = None


class Cu24Driver:
    """High level abstraction for the KR-CU24 RS485 controller."""

    def __init__(self, transport: "Rs485Transport"):
        self.transport = transport

    async def scan(self, addresses: Iterable[int]) -> dict[int, CommandResult]:
        results: dict[int, CommandResult] = {}
        for addr in addresses:
            result = await self.get_version(addr)
            results[addr] = result
        return results

    async def get_version(self, address: int) -> CommandResult:
        frame = self.transport.build_frame(address, 0x00, 0x8F, b"")
        LOGGER.debug("TX %s", frame.hex())
        data = await self.transport.send(frame)
        return CommandResult(success=bool(data), payload=data)

    async def get_status(self, address: int) -> CommandResult:
        frame = self.transport.build_frame(address, 0x00, 0x80, b"")
        LOGGER.debug("TX %s", frame.hex())
        data = await self.transport.send(frame)
        return CommandResult(success=bool(data), payload=data)

    async def unlock(self, address: int, lock_num: int, duration_ms: int) -> CommandResult:
        payload = duration_ms.to_bytes(2, "big")
        frame = self.transport.build_frame(address, lock_num, 0x81, payload)
        LOGGER.debug("TX %s", frame.hex())
        data = await self.transport.send(frame)
        return CommandResult(success=bool(data), payload=data)


class Rs485Transport:
    """Mock transport using asyncio to emulate serial line communication."""

    async def send(self, frame: bytes) -> bytes:
        await asyncio.sleep(0.05)
        LOGGER.debug("RX ack for %s", frame.hex())
        return b"\x10"

    def build_frame(self, address: int, lock_num: int, command: int, payload: bytes) -> bytes:
        data = bytes([0x02, address, lock_num, command, 0x00, len(payload)]) + payload + b"\x03"
        checksum = sum(data) & 0xFF
        return data + bytes([checksum])
