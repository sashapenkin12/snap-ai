"""
Exceptions for simple scenarios.
"""

from fastapi import HTTPException, status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)

authorization_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Resource is not available.",
)
