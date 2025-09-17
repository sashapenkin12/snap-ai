"""
FastAPI web app.

Attributes:
    app: FastAPI web app attribute.
"""
from fastapi import FastAPI

from api.routes.health_check import router as health_router
from api.routes.auth import router as auth_router
from api.core.database import Base, engine


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)



app: FastAPI = FastAPI(title='Snap AI', description='Calorie tracker api.')
app.add_event_handler('startup', init_models)
app.include_router(health_router)
app.include_router(auth_router)
