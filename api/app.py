"""
FastAPI web app.

Attributes:
    app: FastAPI web app attribute.
"""
from fastapi import FastAPI

app: FastAPI = FastAPI(title='Snap AI', description='Calorie tracker api.')
