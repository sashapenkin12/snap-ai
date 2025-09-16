"""
Dependencies for FastAPI routes.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from api.core.database import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession]:
    """
    Generator for database sessions.

    Yields:
        session: Session for working with database
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
