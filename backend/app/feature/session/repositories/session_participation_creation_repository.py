from typing import Protocol

from app.domain.session.session_entity import (
    NewSessionParticipationEntity
)


class SessionParticipationCreationRepoPort(Protocol):
    async def create_participation(
        self,
        participation: NewSessionParticipationEntity
    ) -> None:
        ...
