"""
Service dependency providers.

Purpose
-------
Provide application service instances through FastAPI's dependency injection system.

Responsibilities
----------------
- Construct application service objects.
- Inject repository dependencies into services.

Non-Responsibilities
--------------------
- Business logic.
- Repository implementation.
- HTTP request handling.
"""

from fastapi import Depends

from app.dependencies.repositories import (
    get_incident_repository,
)
from app.repositories import IncidentRepository
from app.services import IncidentService


def get_incident_service(
    repository: IncidentRepository = Depends(
        get_incident_repository
    ),
) -> IncidentService:
    """
    Provide an IncidentService instance.
    """

    return IncidentService(repository)
