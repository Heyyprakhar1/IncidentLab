"""
IncidentLab API application.

Purpose
-------
Compose and configure the FastAPI application.

Responsibilities
----------------
- Create the FastAPI application.
- Register application lifecycle management.
- Register middleware.
- Register API routers.

Non-Responsibilities
--------------------
- Business logic
- API endpoint implementation
- Logging configuration
- Application configuration

Notes
-----
This module is the application's composition root.

It wires together the platform's components while delegating
implementation details to their respective modules.
"""

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.config import settings
from app.lifespan import lifespan
from app.middleware.request_logging import RequestLoggingMiddleware

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)

# Register middleware.
app.add_middleware(RequestLoggingMiddleware)

# Register API routes.
app.include_router(api_router)