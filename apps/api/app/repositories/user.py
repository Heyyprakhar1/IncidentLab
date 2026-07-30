"""
User repository.

Purpose
-------
Encapsulate all database operations related to users.

Responsibilities
----------------
- Retrieve users by ID or email.
- Create new users.
- Check whether an email already exists.

Non-Responsibilities
--------------------
- Password hashing.
- Business validation.
- Authentication.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Repository for user database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """Return a user by ID."""

        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Return a user by email."""

        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        """Return True if a user with the given email already exists."""

        user = await self.get_by_email(email)
        return user is not None

    async def create(
        self,
        *,
        email: str,
        password_hash: str,
    ) -> User:
        """Create a new user."""

        user = User(
            email=email,
            password_hash=password_hash,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user
