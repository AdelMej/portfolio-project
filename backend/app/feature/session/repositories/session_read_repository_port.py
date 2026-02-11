from typing import Protocol
from uuid import UUID

from app.domain.session.session_entity import SessionEntity


class SessionReadRepositoryPort(Protocol):
    async def get_session_by_id(
        self,
        session_id: UUID
    ) -> SessionEntity | None:
        ...

    async def list_sessions(
        self,
        coach_id: UUID
    ) -> list[SessionEntity]:
        ...

    async def get_attendance(
        self,
        session_id: UUID
    ) -> list[SessionEntity]:
        ...
