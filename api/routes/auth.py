"""
Authentication routes.
"""
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr

from api.dependencies.session import get_session
from api.dependencies.user import get_current_user
from api.models.user import User
from api.schemas.user import UserCreate, UserResponse
from api.schemas.token import AccessRefreshToken
from api.services.user import UserService
from api.utils.tokens import get_access_token, get_refresh_token


router = APIRouter(prefix='/auth')


@router.post('/login/', response_model=AccessRefreshToken)
async def login_for_access_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    email: str = await UserService.authenticate(
        form_data=credentials, session=session)
    
    payload = {'sub': email}
    access_token, refresh_token = get_access_token(data=payload), get_refresh_token(data=payload)
    return AccessRefreshToken(
        access_token=access_token, 
        refresh_token=refresh_token,
    )


@router.post('/signup/', response_model=UserResponse)
async def register(
    credentials: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    new_user = await UserService.create_user(user=credentials, session=session)

    return new_user


@router.get('/', response_model=UserResponse)
async def get_about_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
