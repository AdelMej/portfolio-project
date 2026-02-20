from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.domain.session.session_status import SessionStatus


class AdminSessionOutputDTO(BaseModel):
    id: UUID
    coach_id: UUID
    title: str
    starts_at: datetime
    ends_at: datetime
    status: SessionStatus
    cancelled_at: datetime | None
    price_cents: int
    currency: str
    created_at: datetime
    updated_at: datetime


class PaginatedAdminSessionOutputDTO(BaseModel):
    items: list[AdminSessionOutputDTO]
    limit: int
    offset: int
    has_more: bool


class UserProfileOutputDTO(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    attended: bool
