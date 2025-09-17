from typing import Annotated, Optional

from fastapi import Request, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.session import get_session
from api.models.user import User
from api.services.user import UserService
from api.utils.exceptions import authorization_exception
from api.utils.tokens import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    payload = decode_token(token=token)
    identifier: Optional[str] = payload.get('sub')
    user = await UserService.get_user_by_identifier(
        identifier=identifier,
        session=session,
    )
    if not user:
        raise authorization_exception
    return user
