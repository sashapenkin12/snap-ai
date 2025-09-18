from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from api.tests.config import settings

test_engine: AsyncEngine = create_async_engine(
    url=settings.DB_URL,
)

AsyncSessionTest = async_sessionmaker(
    bind=test_engine, autoflush=False,
    expire_on_commit=False, class_=AsyncSession,
)
