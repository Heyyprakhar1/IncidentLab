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

from app.config import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health():
    """
    Return the current health status of the API.
    """

    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }
