"""
Database ORM base.

Purpose
-------
Provide the declarative base class for all SQLAlchemy ORM models.

Responsibilities
----------------
- Define the application's shared ORM base class.
- Register ORM models for SQLAlchemy metadata discovery.

Non-Responsibilities
--------------------
- Database connections.
- Session management.
- Business logic.
- Query execution.

Notes
-----
Every ORM model in IncidentLab should inherit from this base.

Importing `app.models` at the end of this module ensures that all
ORM models are registered with SQLAlchemy's metadata. This is
required for Alembic autogeneration.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all ORM models.
    """

    pass


# Import models so SQLAlchemy metadata discovers them.
from app.models import *  # noqa: F401,F403,E402