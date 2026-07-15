"""
HTTP request logging middleware.

Purpose
-------
Emit one operational log entry for every HTTP request.

Responsibilities
----------------
- Measure request duration.
- Capture request metadata.
- Emit a consistent operational log.

Non-Responsibilities
--------------------
- Authentication
- Authorization
- Business logic
- Exception handling
"""

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.logging_config import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log every HTTP request handled by the application.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "%s %s | status=%s | duration=%.2f ms | client=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            client_ip,
        )

        return response
