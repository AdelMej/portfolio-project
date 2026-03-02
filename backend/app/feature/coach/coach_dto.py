from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class CoachStripeAccountCreationOutputDTO(BaseModel):
    onboarding_url: str | None


class CoachDto(BaseModel):
    first_name: str
    last_name: str


class ParticipationOutputDTO(BaseModel):
    first_name: str
    last_name: str


class GetSessionOutputDto(BaseModel):
    id: UUID
    coach: CoachDto
    title: str
    starts_at: datetime
    ends_at: datetime
    price_cents: int
    currency: str
    status: str
    participants: list[ParticipationOutputDTO]


class PaginatedSessionsOutputDTO(BaseModel):
    items: list[GetSessionOutputDto]
    limit: int
    offset: int
    has_more: bool
