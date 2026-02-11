from typing import Protocol
from uuid import UUID

from app.domain.session.session_entity import SessionEntity


class SessionUpdateRepositoryPort(Protocol):

    async def update_session(
        self,
        session: SessionEntity
    ) -> SessionEntity: ...

    async def cancel_session(
            self,
            session_id: UUID
    ) -> bool:
        ...
