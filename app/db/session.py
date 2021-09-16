from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

# TODO: echo False in prod
engine = create_async_engine(
    settings.POSTGRES_DATABASE_URI,
    echo=True,
    future=True
)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    return sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
