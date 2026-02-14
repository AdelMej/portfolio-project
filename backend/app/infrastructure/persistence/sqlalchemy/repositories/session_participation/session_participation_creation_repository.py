from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.session.session_entity import NewSessionParticipationEntity
from app.feature.session.repositories import (
    SessionParticipationCreationRepoPort
)


class SqlAlchemySessionParticipationCreationRepo(
    SessionParticipationCreationRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_participation(
        self,
        participation: NewSessionParticipationEntity
    ) -> None:
        ...
