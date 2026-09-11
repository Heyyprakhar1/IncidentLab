"""
Exception exports.

Purpose
-------
Provide a single import location for application exceptions.

Responsibilities
----------------
- Expose public exception classes.
- Simplify exception imports across application layers.

Non-Responsibilities
--------------------
- Define exception behavior.
- Handle exception conversion.
"""

from app.exceptions.base import IncidentLabException
from app.exceptions.incident import IncidentNotFoundException

__all__ = [
    "IncidentLabException",
    "IncidentNotFoundException",
]
