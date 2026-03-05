from datetime import datetime
from uuid import UUID
from app.domain.session.session_status import SessionStatus
from dataclasses import dataclass

from app.domain.user.user_profile_entity import UserProfileEntity


@dataclass(frozen=True)
class SessionEntity:
    id: UUID
    coach_id: UUID
    title: str
    starts_at: datetime
    ends_at: datetime
    status: SessionStatus
    cancelled_at: datetime
    price_cents: int
    currency: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class NewSessionEntity:
    coach_id: UUID
    title: str
    starts_at: datetime
    ends_at: datetime
    price_cents: int
    currency: str


@dataclass(frozen=True)
class SessionWithCoachEntity:
    id: UUID
    coach: UserProfileEntity
    title: str
    starts_at: datetime
    ends_at: datetime
    status: SessionStatus
    cancelled_at: datetime
    price_cents: int
    currency: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class SessionCompleteEntity:
    id: UUID
    coach: UserProfileEntity
    title: str
    starts_at: datetime
    ends_at: datetime
    status: SessionStatus
    cancelled_at: datetime
    price_cents: int
    currency: str
    created_at: datetime
    updated_at: datetime
    participants: list[UserProfileEntity]
