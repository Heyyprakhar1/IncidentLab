"""
Error response schemas.

Purpose
-------
Define standardized error response contracts for IncidentLab APIs.

Responsibilities
----------------
- Define public error response structure.
- Provide typed API error contracts.
- Maintain consistency across API failures.

Non-Responsibilities
--------------------
- Exception handling logic.
- HTTP status code mapping.
- Business error generation.

Notes
-----
Error schemas represent the public API contract.

They allow clients to consume predictable error responses
regardless of which internal layer generated the error.
"""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """
    Represents individual error information.
    """

    code: str
    message: str


class ErrorResponse(BaseModel):
    """
    Standard API error response.

    All application errors exposed through the API
    should follow this structure.
    """

    error: ErrorDetail
