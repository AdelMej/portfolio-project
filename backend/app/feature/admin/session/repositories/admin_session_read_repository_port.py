from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.session.session_entity import SessionEntity


class AdminSessionReadRepoPort(Protocol):
    async def sessions_by_coach_id(
        self,
        coach_id: UUID,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionEntity], bool]:
        ...

    async def get_all_sessions(
        self,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionEntity], bool]:
        ...

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

    async def is_session_started(
        self,
        session_id: UUID
    ) -> bool:
        ...
