"""
Utilities for security serving.
"""

from typing import Any
from datetime import timedelta, datetime, timezone

from jwt import decode, encode
from jwt.exceptions import InvalidTokenError

from api.core.config import settings
from api.utils.exceptions import credentials_exception


def decode_token(
    token: str,
    type: str = 'access', 
    raise_exception: bool = True,
) -> dict[str, Any]:
    """
    Decodes and verifies JWT token.

    Args:
        token: JWT encoded token.
    
    Returns:
        str: Encoded token.

    Raises:
        credentials_exception: If token isn't valid.
    """
    try:
        payload = decode(
            token, settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get('token_type') != type:
            raise InvalidTokenError
        return payload
    except InvalidTokenError:
        if not raise_exception:
            return dict()
        raise credentials_exception


def _create_token(
    data: dict,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    """
    Factory function that creates encoded token.

    Args:
        data: Dictionary with data to store in the token
        expire_delta: Delta time for token lifespan.
        token_type: Type of token, access or refresh.

    Returns:
        str: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "token_type": token_type})
    return encode(
        to_encode, settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def get_access_token(data: dict) -> str:
    """
    Get new JWT access token.

    Args:
        data: Token payload.

    Returns:
        str: Encoded JWT access token.
    """
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return _create_token(
        data=data,
        expires_delta=expires_delta,
        token_type='access',
    )


def get_refresh_token(data: dict) -> str:
    """
    Get new JWT refresh token.

    Args:
        data: Token payload.

    Returns:
        str: Encoded JWT refresh token.
    """
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    return _create_token(
        data=data,
        expires_delta=expires_delta,
        token_type='refresh',
    )


def refresh_access_token(refresh_token: str) -> str:
    """
    Get new JWT access token with the refresh token.

    Args:
        refresh_token: JWT refresh token.
    
    Returns:
        str: New access token.

    Raises:
        credentials_exception: If token isn't valid.
    """
    payload = decode_token(token=refresh_token, type='refresh')

    sub = payload.get('sub')
    if not sub:
        raise credentials_exception
     
    return get_access_token(data={'sub': sub})
