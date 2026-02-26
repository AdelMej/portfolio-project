from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class SessionParticipationEntity():
    id: UUID
    session_id: UUID
    user_id: UUID
    paid_at: datetime
    registred_at: datetime
    cancelled_at: datetime
    expires_at: datetime


@dataclass(frozen=True)
class NewSessionParticipationEntity():
    session_id: UUID
    user_id: UUID
