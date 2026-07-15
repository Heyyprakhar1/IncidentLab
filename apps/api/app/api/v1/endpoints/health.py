"""
Health API endpoints.

Purpose
-------
Expose endpoints used to verify the operational health of the API.

Responsibilities
----------------
- Report application availability.
- Return basic runtime information.

Non-Responsibilities
--------------------
- Business logic
- Infrastructure health checks
- Dependency validation

Notes
-----
This router intentionally provides only a basic health endpoint.

As IncidentLab evolves, deeper health checks (database, cache,
external services, etc.) may be added without affecting unrelated
API resources.
"""

from fastapi import APIRouter

from app.schemas import HealthResponse
from app.services import HealthService

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

health_service = HealthService()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Return the operational status of the IncidentLab API.",
)
async def health() -> HealthResponse:
    """
    Return the current health status of the API.
    """

    return health_service.get_health()
