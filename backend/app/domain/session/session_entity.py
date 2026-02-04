from datetime import datetime
from uuid import UUID
from app.domain.session.session_status import SessionStatus
from dataclasses import dataclass


@dataclass(frozen=True)
class SessionEntity:

    id:UUID
    coach_id:UUID
    title:str
    starts_at:datetime
    ends_at:datetime
    status:SessionStatus

    def cancel(self) -> "SessionEntity":
        if self.status == SessionStatus.CANCELLED:
            return self  # idempotent

        return SessionEntity(
            id=self.id,
            coach_id=self.coach_id,
            title=self.title,
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            status=SessionStatus.CANCELLED,
        )