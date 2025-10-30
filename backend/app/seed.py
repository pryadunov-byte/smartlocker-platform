"""CLI entry for seeding demo data."""
from __future__ import annotations

import asyncio

from .db.session import async_session
from .services.seeds import seed_demo


async def main() -> None:
    async with async_session() as session:
        await seed_demo(session)


if __name__ == "__main__":
    asyncio.run(main())
