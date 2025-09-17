from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.session import get_session

router = APIRouter(prefix='/health')

@router.get('/')
async def health_check(session: AsyncSession = Depends(get_session)) -> dict[str, Any]:
    try:
        result = await session.execute(text("SELECT version()"))
        version = result.scalar()
        return {
            "status": "ok",
            "db_version": version,
        }
    except SQLAlchemyError as exception:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {exception}")
