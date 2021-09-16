import asyncpg
from fastapi import FastAPI
from loguru import logger

from app.core.config import settings

# TODO: add missing env variables
async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(settings.POSTGRES_DATABASE_URI))

    app.state.pool = await asyncpg.create_pool(
        str(settings.POSTGRES_DATABASE_URI),
        min_size=settings.MIN_CONNECTIONS_COUNT,
        max_size=settings.MAX_CONNECTIONS_COUNT,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
