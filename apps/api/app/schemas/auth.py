"""
Authentication API schemas.

Purpose
-------
Define request and response schemas for authentication workflows.

Responsibilities
----------------
- Validate authentication requests.
- Define authentication responses.
- Represent JWT payloads.

Non-Responsibilities
--------------------
- Password hashing.
- JWT generation.
- Database operations.
"""

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """
    User registration request.
    """

    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """
    User login request.
    """

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    JWT access token response.
    """

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    JWT token payload.
    """

    sub: str
    exp: int
