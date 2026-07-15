"""
Application lifecycle management.

Purpose
-------
Own the application's startup and shutdown lifecycle.

Responsibilities
----------------
- Initialize platform-level services.
- Emit application lifecycle events.
- Release shared resources during shutdown.

Non-Responsibilities
--------------------
- HTTP request handling
- Route registration
- Business logic
- Application configuration

Notes
-----
This module acts as the application's orchestration layer.

As IncidentLab evolves, shared platform resources such as database
connections, cache clients, cloud SDKs, and background workers will
be initialized and cleaned up here.

Business logic should never live in this module.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.logging_config import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application's lifecycle.

    The `app` parameter is currently unused, but it is intentionally
    retained because future shared resources may be attached to the
    FastAPI application instance during startup.
    """

    # Configure the application's logging system.
    configure_logging()

    logger.info(
        "Starting IncidentLab API (environment=%s, version=%s)",
        settings.app_env,
        settings.app_version,
    )

    try:
        yield

    finally:
        logger.info("Stopping IncidentLab API.")
