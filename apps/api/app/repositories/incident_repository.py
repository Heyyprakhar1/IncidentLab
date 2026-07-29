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
        """
        Initialize the repository.

        Parameters
        ----------
        db:
            Active SQLAlchemy asynchronous database session.
        """
        self.db = db

    async def create(
        self,
        incident: Incident,
    ) -> Incident:
        """
        Persist a new incident.

        Responsibilities
        ----------------
        - Insert a new incident.
        - Commit the transaction.
        - Refresh the ORM object.

        Returns
        -------
        Incident
            The persisted incident.
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

        Responsibilities
        ----------------
        - Fetch all persisted incidents.

        Returns
        -------
        list[Incident]
            Collection of persisted incidents.
        """

        result = await self.db.execute(
            select(Incident)
        )

        return result.scalars().all()
