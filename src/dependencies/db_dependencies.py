from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from fastapi import Depends
from typing import Annotated, AsyncGenerator
from db.main import get_async_session


# Dependency alias for FastAPI
SessionDependency: Annotated[AsyncSession, Depends(get_async_session)] = Depends(
    get_async_session
)
