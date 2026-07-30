"""
Exception handlers.

Purpose
-------
Convert application exceptions into standardized API responses.

Responsibilities
----------------
- Handle application-level exceptions.
- Map exceptions to HTTP responses.
- Return consistent error contracts.
- Register global exception handlers.

Non-Responsibilities
--------------------
- Generate business exceptions.
- Contain business logic.
- Perform database operations.

Notes
-----
This module acts as the boundary between application errors
and HTTP responses.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.base import IncidentLabException
from app.schemas import ErrorResponse


async def incidentlab_exception_handler(
    request: Request,
    exc: IncidentLabException,
) -> JSONResponse:
    """
    Handle application-level exceptions.

    Converts internal application errors into
    standardized API error responses.
    """

    response = ErrorResponse(
        error={
            "code": exc.code,
            "message": exc.message,
        }
    )

    return JSONResponse(
        status_code=exc.status_code,   # <-- BAS YE LINE
        content=response.model_dump(),
    )


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register application exception handlers.
    """

    app.add_exception_handler(
        IncidentLabException,
        incidentlab_exception_handler,
    )
