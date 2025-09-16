"""
Main ORM attributes.

Attributes:
    engine: Async SQLAlchemy engine with database url from environment settings.
    AsyncSessionLocal: Async session maker.
    Base: Base class for declarative class definitions.
"""
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from api.core.config import settings

engine: AsyncEngine = create_async_engine(url=settings.DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, autoflush=False,
    expire_on_commit=False, class_=AsyncSession,
)

Base = declarative_base()
