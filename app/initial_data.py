import logging
import asyncio

from app.db.init_db import init_db
from app.db.session import get_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async_session = await get_session()
    async with async_session() as db:
        print(db)
        await init_db(db)

async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
