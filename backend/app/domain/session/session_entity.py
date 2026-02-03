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
