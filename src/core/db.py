from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core import settings


async_engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def results_to_dict(result):
    rows = result.scalars().all()
    return [dict(row) for row in rows]
