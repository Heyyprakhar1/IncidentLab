"""
Repository dependency providers.

Purpose
-------
Provide repository instances through FastAPI's dependency injection system.

Responsibilities
----------------
- Construct repository objects.
- Inject database sessions into repositories.

Non-Responsibilities
--------------------
- Business logic.
- Database session creation.
- HTTP request handling.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import IncidentRepository


def get_incident_repository(
    db: AsyncSession = Depends(get_db),
) -> IncidentRepository:
    """
    Provide an IncidentRepository instance.
    """

    return IncidentRepository(db)
