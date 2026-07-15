"""
Health application service.

Purpose
-------
Provide application health information.

Responsibilities
----------------
- Build the health response.
- Encapsulate health-related application logic.

Non-Responsibilities
--------------------
- HTTP request handling.
- Configuration management.
- Response serialization.

Notes
-----
As IncidentLab evolves, this service may incorporate checks for
databases, caches, cloud services, and other platform dependencies.
"""

from app.config import settings
from app.schemas import HealthResponse


class HealthService:
    """
    Application service responsible for health operations.
    """

    def get_health(self) -> HealthResponse:
        """
        Return the current health status of the application.
        """

        return HealthResponse(
            status="healthy",
            service=settings.app_name,
            version=settings.app_version,
            environment=settings.app_env,
        )
