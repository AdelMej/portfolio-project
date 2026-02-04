from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from app.domain.auth.role import Role
from pydantic.networks import EmailStr
from app.shared.rules.email_rules import (
    MIN_EMAIL_LENGTH,
    MAX_EMAIL_LENGTH
)


class UserDTO(BaseModel):
    id: UUID
    email: EmailStr = Field(
        ...,
        min_length=MIN_EMAIL_LENGTH,
        max_length=MAX_EMAIL_LENGTH
    )
    roles: set[Role]
    disabled_at: datetime | None
    created_at: datetime


class PaginatedUsersDTO(BaseModel):
    items: list[UserDTO]
    limit: int
    offset: int
    has_more: bool
