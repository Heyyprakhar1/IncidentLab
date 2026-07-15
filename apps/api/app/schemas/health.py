"""
Health response schemas.

Purpose
-------
Define the public API contract for health-related endpoints.

Responsibilities
----------------
- Describe health response models.
- Provide typed API responses.
- Serve as the single source of truth for response structure.

Non-Responsibilities
--------------------
- Business logic
- HTTP request handling
- Configuration
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Response returned by the health endpoint.
    """

    status: str
    service: str
    version: str
    environment: str
