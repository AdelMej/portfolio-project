from datetime import datetime
from uuid import UUID
from app.domain.session.session_status import SessionStatus

class SessionEntity:
    def __init__(
        self,
        id: UUID,
        coach_id: UUID,
        title: str,
        starts_at: datetime,
        end_at: datetime,
        status: SessionStatus
    ):
        self.id = id
        self.coach_id = coach_id
        self.title = title
        self.starts_at = starts_at
        self.end_at = end_at
        self.status = status
