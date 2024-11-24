import subprocess
from collections.abc import AsyncGenerator, Callable

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker

from src.settings.configuration import config_project


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=False, pool_pre_ping=True)


async_session_maker: Callable[..., AsyncSession] = sessionmaker(
    create_async_engine(config_project.postgres_db.build_connection()),
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


async def migrate() -> None:
    subprocess.run("alembic upgrade head", shell=True, check=True)
