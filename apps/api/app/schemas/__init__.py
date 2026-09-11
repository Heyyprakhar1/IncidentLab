"""
Schema exports.

Purpose
-------
Provide a single import location for API schemas.

Responsibilities
----------------
- Expose public schema classes.
- Simplify imports across application layers.

Non-Responsibilities
--------------------
- Define schema behavior.
- Handle validation logic.
"""

from app.schemas.error import ErrorDetail, ErrorResponse
from app.schemas.health import HealthResponse
from app.schemas.incident import IncidentCreate, IncidentResponse

__all__ = [
    "ErrorDetail",
    "ErrorResponse",
    "HealthResponse",
    "IncidentCreate",
    "IncidentResponse",
]
