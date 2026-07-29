"""
Incident repository.

Purpose
-------
Provide data-access operations for Incident entities.

Responsibilities
----------------
- Persist Incident objects.
- Retrieve Incident objects.
- Update Incident objects.
- Delete Incident objects.
- Encapsulate all database interaction for Incident entities.

Non-Responsibilities
--------------------
- Business logic.
- Request validation.
- API response formatting.
- Database session creation.

Notes
-----
Repositories isolate SQLAlchemy operations from the service layer.

Application services should interact with repositories instead of
issuing ORM queries directly.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import Incident


class IncidentRepository:
    """
    Repository responsible for Incident persistence.
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        incident: Incident,
    ) -> Incident:
        """
        Persist a new incident.
        """

        self.db.add(incident)

        await self.db.commit()

        await self.db.refresh(incident)

        return incident

    async def list(
        self,
    ) -> list[Incident]:
        """
        Retrieve all incidents.
        """

        result = await self.db.execute(
            select(Incident)
        )

        return result.scalars().all()

    async def get_by_id(
        self,
        incident_id: int,
    ) -> Incident | None:
        """
        Retrieve a single incident by identifier.

        Responsibilities
        ----------------
        - Fetch an incident by its identifier.

        Returns
        -------
        Incident | None
            The matching incident if it exists;
            otherwise None.
        """

        result = await self.db.execute(
            select(Incident).where(
                Incident.id == incident_id
            )
        )

        return result.scalar_one_or_none()
