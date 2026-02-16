from typing import Protocol

from app.domain.session.session_entity import (
    NewSessionEntity,
)


class SessionCreationRepoPort(Protocol):
    async def create_session(
        self,
        session: NewSessionEntity
    ) -> None:
        ...
