"""
Dependency providers.

Purpose
-------
Expose dependency providers used throughout the application.

Responsibilities
----------------
- Export database dependencies.
- Export repository dependencies.
- Export service dependencies.

Non-Responsibilities
--------------------
- Business logic.
- Dependency implementation.
"""

from app.dependencies.database import get_db
from app.dependencies.repositories import (
    get_incident_repository,
)
from app.dependencies.services import (
    get_incident_service,
)

__all__ = [
    "get_db",
    "get_incident_repository",
    "get_incident_service",
]
