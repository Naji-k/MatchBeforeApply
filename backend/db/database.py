from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from core.config import settings

""" Database setup using SQLAlchemy with async support. Defines the engine, session, and base class for models."""


def get_engine():
    socket_path = settings.CLOUD_SQL_SOCKET

    connect_args = {}

    if socket_path:
        connect_args = {
            "host": socket_path,
        }

    return create_async_engine(
        settings.ASYNC_DATABASE_URL,
        connect_args=connect_args,
        echo=False,
        pool_pre_ping=True,
    )


engine = get_engine()
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """Dependency that provides a database session to API routes. Ensures proper cleanup after use."""
    async with SessionLocal() as session:
        yield session
