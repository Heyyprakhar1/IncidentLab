"""
API v1 router.

Purpose
-------
Aggregate and expose all version 1 API routes.

Responsibilities
----------------
- Register API endpoint routers.
- Define the API version prefix.
- Provide a single entry point for version 1 routes.

Non-Responsibilities
--------------------
- Business logic
- HTTP request handling
- Application configuration

Notes
-----
Each API resource owns its own router.

This module composes those routers into the public Version 1 API.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.incident import router as incident_router


api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(health_router)
api_router.include_router(incident_router)
