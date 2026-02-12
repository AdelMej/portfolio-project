from typing import Protocol

from app.domain.session.session_entity import NewSessionEntity


class SessionCreationRepositoryPort(Protocol):
    async def create_session(
        self,
        session: NewSessionEntity
    ) -> None:
        ...
