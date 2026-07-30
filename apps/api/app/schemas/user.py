"""
User API schemas.

Purpose
-------
Define request and response schemas for user-related operations.

Responsibilities
----------------
- Validate incoming user data.
- Define user response models.
- Serialize user objects returned by the API.

Non-Responsibilities
--------------------
- Database models.
- Password hashing.
- Authentication logic.
- Business rules.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """

    email: EmailStr

    password: str


class UserResponse(BaseModel):
    """
    Public user representation returned by the API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    email: EmailStr

    is_active: bool

    created_at: datetime

    updated_at: datetime
