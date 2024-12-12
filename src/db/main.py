from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from typing import AsyncGenerator
from os import getenv


engine: AsyncEngine
async_session: async_sessionmaker


def init_db():
    global engine, async_session

    # Database connection URL
    DATABASE_URL = getenv("DATABASE_URL")

    # Create the asynchronous engine
    engine = create_async_engine(DATABASE_URL, echo=True, future=True)

    # Create the session factory
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )


# Dependency to get the async session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
