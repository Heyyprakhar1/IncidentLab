"""
Database infrastructure.

Purpose
-------
Provide a centralized SQLAlchemy database engine and session factory.

Responsibilities
----------------
- Create the asynchronous database engine.
- Create database sessions.
- Provide a FastAPI database dependency.

Non-Responsibilities
--------------------
- Database models.
- Business logic.
- Database migrations.
- Query execution.

Notes
-----
This module acts as the single source of truth for database access.

All application services should obtain database sessions through
the `get_db()` dependency rather than creating their own sessions.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.db_user}:"
    f"{settings.db_password}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield a database session.

    The session is automatically closed after the request
    has been processed.
    """

    async with SessionLocal() as session:
        yield session