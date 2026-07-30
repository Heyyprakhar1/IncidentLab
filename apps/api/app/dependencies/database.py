"""
Database dependency providers.

Purpose
-------
Expose database dependencies used throughout the application.

Responsibilities
----------------
- Re-export the application's database session dependency.

Non-Responsibilities
--------------------
- Session creation.
- Engine configuration.
- Business logic.
"""

from app.core.database import get_db

__all__ = ["get_db"]
