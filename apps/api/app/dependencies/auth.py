"""
Authentication dependencies.

Purpose
-------
Provide dependency injection helpers for authentication services.

Responsibilities
----------------
- Provide authentication service instances.
- Validate JWT access tokens.
- Resolve the currently authenticated user.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import decode_access_token
from app.dependencies.database import get_db
from app.repositories.user import UserRepository
from app.services.auth import AuthService

security = HTTPBearer()


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    """
    Return a UserRepository instance.
    """
    return UserRepository(db)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """
    Return an AuthService instance.
    """
    return AuthService(user_repository)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    user_repository: UserRepository = Depends(
        get_user_repository
    ),
):
    """
    Return the currently authenticated user.
    """

    try:
        payload = decode_access_token(
            credentials.credentials
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        ) from exc

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload.",
        )

    user = await user_repository.get_by_id(
        int(user_id)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return user
