"""
Application logging configuration.

Purpose
-------
Configure how IncidentLab emits operational logs.

Responsibilities
----------------
- Configure the root logger.
- Set the application log level.
- Define a consistent log format.

Non-Responsibilities
--------------------
- Log business events.
- Handle HTTP requests.
- Read environment variables directly.
- Contain application logic.

Notes
-----
Configuration values are provided through `app.config`,
maintaining a Single Source of Truth (SSOT).

This module only defines *how* the application logs.
It does not decide *what* should be logged.
"""

import logging

from app.config import settings


logger = logging.getLogger("incidentlab")


def configure_logging() -> None:
    """
    Configure the application's logging system.

    This function should be called once during application startup
    before the API begins handling requests.
    """

    logging.basicConfig(
        level=settings.log_level.upper(),
        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
    )
