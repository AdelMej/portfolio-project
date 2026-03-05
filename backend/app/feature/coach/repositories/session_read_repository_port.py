from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.session.session_entity import SessionCompleteEntity


class SessionReadRepoPort(Protocol):
    async def exist_session(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def is_session_owner(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        ...

    async def is_session_cancelled(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def is_session_finished(
        self,
        session_id: UUID
    ) -> bool:
        ...

    async def get_complete_session_by_id(
        self,
        session_id: UUID
    ) -> SessionCompleteEntity:
        ...

    async def get_own_coach_sessions(
        self,
        user_id: UUID,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionCompleteEntity], bool]:
        ...
