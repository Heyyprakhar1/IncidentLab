"""
Authentication service.

Purpose
-------
Handle authentication business logic.

Responsibilities
----------------
- Register new users.
- Authenticate existing users.
- Generate JWT access tokens.

Non-Responsibilities
--------------------
- HTTP responses.
- Database implementation.
- Password hashing implementation.
"""

from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.repositories.user import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class UserAlreadyExistsError(Exception):
    """Raised when email is already registered."""


class AuthService:
    """Authentication service."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(
        self,
        request: RegisterRequest,
    ) -> UserResponse:
        """
        Register a new user.
        """

        if await self.repository.email_exists(request.email):
            raise UserAlreadyExistsError(
                "Email is already registered."
            )

        password_hash = hash_password(request.password)

        user = await self.repository.create(
            email=request.email,
            password_hash=password_hash,
        )

        return UserResponse.model_validate(user)

    async def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:
        """
        Authenticate user and issue JWT.
        """

        user = await self.repository.get_by_email(request.email)

        if user is None:
            raise AuthenticationError(
                "Invalid email or password."
            )

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise AuthenticationError(
                "Invalid email or password."
            )

        token = create_access_token(
            subject=str(user.id),
        )

        return TokenResponse(
            access_token=token,
        )
