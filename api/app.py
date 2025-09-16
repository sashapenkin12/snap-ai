"""
FastAPI web app.

Attributes:
    app: FastAPI web app attribute.
"""
from fastapi import FastAPI

from api.routes.health_check import router as health_router

app: FastAPI = FastAPI(title='Snap AI', description='Calorie tracker api.')

app.include_router(health_router)
