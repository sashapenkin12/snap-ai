import asyncio

import pytest_asyncio

from api.core.database import Base
from api.tests.test_db import test_engine, AsyncSessionTest


@pytest_asyncio.fixture(scope='session')
async def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close() 


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionTest() as session:
        yield session
        await session.rollback()
