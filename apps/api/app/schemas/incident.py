"""
Incident schemas.

Purpose
-------
Define request and response contracts for Incident APIs.

Responsibilities
----------------
- Validate incoming API data.
- Serialize outgoing API data.

Non-Responsibilities
--------------------
- Business logic.
- Database persistence.
- HTTP routing.

Notes
-----
These schemas define the public API contract for Incident resources.
"""

from pydantic import BaseModel


class IncidentCreate(BaseModel):
    """
    Request schema for creating an incident.
    """

    title: str
    description: str
    severity: str


class IncidentResponse(BaseModel):
    """
    Response schema for an incident.
    """

    id: int
    title: str
    description: str
    severity: str
    status: str

    model_config = {
        "from_attributes": True,
    }
