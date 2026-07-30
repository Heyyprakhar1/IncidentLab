"""
Incident application service.

Purpose
-------
Provide application services for Incident resources.

Responsibilities
----------------
- Coordinate incident-related business operations.
- Delegate persistence to the repository layer.
- Return API response models.

Non-Responsibilities
--------------------
- HTTP request handling.
- Database queries.
- ORM model definitions.

Notes
-----
The service layer represents the application's business use cases.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import IncidentNotFoundException
from app.models import Incident
from app.repositories import IncidentRepository
from app.schemas import IncidentCreate, IncidentResponse


class IncidentService:
    """
    Application service for Incident operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self.repository = IncidentRepository(db)

    async def create_incident(
        self,
        incident: IncidentCreate,
    ) -> IncidentResponse:
        """
        Create a new incident.
        """

        db_incident = Incident(
            title=incident.title,
            description=incident.description,
            severity=incident.severity,
        )

        created_incident = await self.repository.create(
            db_incident
        )

        return IncidentResponse.model_validate(
            created_incident
        )

    async def list_incidents(
        self,
    ) -> list[IncidentResponse]:
        """
        Retrieve all incidents.
        """

        incidents = await self.repository.list()

        return [
            IncidentResponse.model_validate(incident)
            for incident in incidents
        ]

    async def get_incident(
        self,
        incident_id: int,
    ) -> IncidentResponse:
        """
        Retrieve a single incident.
        """

        incident = await self.repository.get_by_id(
            incident_id
        )

        if incident is None:
            raise IncidentNotFoundException(
                incident_id
            )

        return IncidentResponse.model_validate(
            incident
        )
