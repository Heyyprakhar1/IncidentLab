"""
Incident API endpoints.

Purpose
-------
Expose HTTP endpoints for Incident resources.

Responsibilities
----------------
- Accept HTTP requests.
- Validate request payloads.
- Delegate business logic to the service layer.
- Return serialized responses.

Non-Responsibilities
--------------------
- Business logic.
- Database access.
- ORM operations.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import IncidentCreate, IncidentResponse
from app.services import IncidentService

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_incident(
    incident: IncidentCreate,
    db: AsyncSession = Depends(get_db),
) -> IncidentResponse:
    """
    Create a new incident.
    """

    service = IncidentService(db)

    return await service.create_incident(incident)
