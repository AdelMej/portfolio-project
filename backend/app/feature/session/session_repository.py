from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.domain.session.session_entity import SessionEntity
from app.infrastructure.persistence.sqlalchemy.models.sessions import Session as SessionModel


class SessionRepository(Protocol):

    async def get_session_by_id(
        self,
        db: AsyncSession,
        session_id: UUID
    ) -> SessionModel | None: ...

    async def create_session(
        self,
        session: SessionEntity
    ) -> SessionEntity: ...

    async def list_sessions(
        self,
        db: AsyncSession,
        coach_id: UUID | None = None
    ) -> list[SessionModel]: ...

    async def update_session(
        self,
        db: AsyncSession,
        session: SessionModel
    ) -> SessionModel: ...
    