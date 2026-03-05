from datetime import datetime
from typing import Protocol

from app.domain.session_participation.session_participation_entity import (
    NewSessionParticipationEntity
)


class SessionParticipationCreationRepoPort(Protocol):
    async def create_participation(
        self,
        participation: NewSessionParticipationEntity,
        expires_at: datetime
    ) -> None:
        ...
