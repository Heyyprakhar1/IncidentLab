"""
Incident ORM model.

Purpose
-------
Represent incidents stored within the IncidentLab platform.

Responsibilities
----------------
- Define the incident database table.
- Define ORM mappings.
- Represent persisted incident records.

Non-Responsibilities
--------------------
- Business logic.
- Database sessions.
- API schemas.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Incident(Base):
    """
    Incident database entity.
    """

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="open",
    )