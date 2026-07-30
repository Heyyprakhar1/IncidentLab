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

from fastapi import APIRouter, Depends, Path, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_incident_service
from app.models.user import User
from app.schemas import IncidentCreate, IncidentResponse
from app.services import IncidentService

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_incident(
    incident: IncidentCreate,
    current_user: User = Depends(get_current_user),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    """
    Create a new incident.
    """

    # Reserved for future ownership support.
    _ = current_user

    return await service.create_incident(
        incident
    )


@router.get(
    "",
    response_model=list[IncidentResponse],
    status_code=status.HTTP_200_OK,
)
async def list_incidents(
    current_user: User = Depends(get_current_user),
    service: IncidentService = Depends(get_incident_service),
) -> list[IncidentResponse]:
    """
    Retrieve all incidents.
    """

    _ = current_user

    return await service.list_incidents()


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    status_code=status.HTTP_200_OK,
)
async def get_incident(
    incident_id: int = Path(
        ...,
        gt=0,
        description="Unique identifier of the incident.",
    ),
    current_user: User = Depends(get_current_user),
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    """
    Retrieve a single incident by its identifier.
    """

    _ = current_user

    return await service.get_incident(
        incident_id
    )
