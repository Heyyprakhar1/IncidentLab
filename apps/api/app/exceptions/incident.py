"""
Incident domain exceptions.
"""

from fastapi import status

from app.exceptions.base import IncidentLabException


class IncidentNotFoundException(IncidentLabException):
    """
    Raised when an incident cannot be found.
    """

    def __init__(
        self,
        incident_id: int,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="INCIDENT_NOT_FOUND",
            message=f"Incident with id {incident_id} was not found.",
        )
