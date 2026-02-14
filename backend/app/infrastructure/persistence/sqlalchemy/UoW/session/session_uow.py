from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.uow.session_uow_port import (
    SessionUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepo
)
from app.infrastructure.persistence.sqlalchemy.repositories.session import (
    SqlAlchemySessionUpdateRepo,
    SqlAlchemySessionReadRepo,
    SqlAlchemySessionCreationRepo
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemySessionParticipationReadRepo
)


class SqlAlchemySessionUoW(SessionUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.session_creation_repo = SqlAlchemySessionCreationRepo(session)
        self.session_update_repo = SqlAlchemySessionUpdateRepo(session)
        self.session_read_repo = SqlAlchemySessionReadRepo(session)
        self.session_participation_read_repo = (
            SqlAlchemySessionParticipationReadRepo(session)
        )
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
