from datetime import datetime
from typing import Protocol
from uuid import UUID

from app.domain.session.session_entity import SessionEntity


class SessionReadRepositoryPort(Protocol):
    async def get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionEntity | None:
        ...

    async def get_all_sessions(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionEntity], bool]:
        ...

    async def get_sessions_by_coach_id(
        self,
        coach_id: UUID,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None
    ) -> tuple[list[SessionEntity], bool]:
        ...

    async def get_attendance(
        self,
        session_id: UUID
    ) -> list[SessionEntity]:
        ...
