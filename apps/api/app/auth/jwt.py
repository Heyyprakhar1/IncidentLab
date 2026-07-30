"""
JWT utilities.

Purpose
-------
Provide helper functions for creating and decoding JWT access tokens.

Responsibilities
----------------
- Create JWT access tokens.
- Decode and validate JWT access tokens.

Non-Responsibilities
--------------------
- User authentication.
- Database operations.
- Authorization decisions.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from jwt import InvalidTokenError

from app.config import settings


def create_access_token(subject: str) -> str:
    """
    Create a signed JWT access token.
    """
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.
    """
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

    except InvalidTokenError as exc:
        raise ValueError("Invalid or expired token.") from exc
