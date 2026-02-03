from pydantic import BaseModel, Field
from uuid import UUID

from pydantic.networks import EmailStr
from app.shared.rules.email_rules import (
    MIN_EMAIL_LENGTH,
    MAX_EMAIL_LENGTH
)


class GetUserDTO(BaseModel):
    id: UUID
    email: EmailStr = Field(
        ...,
        min_length=MIN_EMAIL_LENGTH,
        max_length=MAX_EMAIL_LENGTH
    )
    first_name: str
    last_name: str
