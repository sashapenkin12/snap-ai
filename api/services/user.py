from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.models.user import User
from api.schemas.user import UserCreate
from api.utils.password import verify_password
from api.utils.exceptions import credentials_exception


class UserService:
    model = User

    @classmethod
    async def get_user_by_identifier(
            cls, identifier: str | Any,
            session: AsyncSession,
        ) -> Optional[User]:
        result = (
            await session.execute(
                select(cls.model).where(
                        (cls.model.email==identifier) | (cls.model.username==identifier)
                    ),
                )
            ).scalar_one_or_none()
                
        return result
    
    @classmethod
    async def create_user(
        cls, user: UserCreate,
        session: AsyncSession,
    ) -> User:
        async with session.begin():
            
            existing_user = await cls.get_user_by_identifier(identifier=user.email, session=session)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this e-mail is already exists."
                )
            
            new_user = user.to_model()

            session.add(new_user)

        return new_user
    
    @classmethod
    async def authenticate(
        cls, form_data: OAuth2PasswordRequestForm,
        session: AsyncSession,
    ) -> str:
        user = await cls.get_user_by_identifier(identifier=form_data.username, session=session)
        if not user:
            raise credentials_exception
        
        is_credentials_correct = verify_password(form_data.password, user.hashed_password)
        if not is_credentials_correct:
            raise credentials_exception
        
        return user.email
