from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.session.session_entity import SessionCompleteEntity


class SessionReadRepoPort(Protocol):
    async def get_own_sessions(
        self,
        user_id: UUID,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionCompleteEntity], bool]:
        ...

    async def get_complete_session_by_id(
        self,
        session_id: UUID
    ) -> SessionCompleteEntity:
        ...
