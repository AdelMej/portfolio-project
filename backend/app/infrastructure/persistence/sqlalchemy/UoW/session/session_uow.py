from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.uow.session_uow_port import (
    SessionUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepository
)
from app.infrastructure.persistence.sqlalchemy.repositories.session import (
    SqlAlchemySessionUpdateRepository,
    SqlAlchemySessionReadRepository,
    SqlAlchemySessionCreationRepository
)


class SqlAlchemySessionUoW(SessionUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.session_creation_repository = (
            SqlAlchemySessionCreationRepository(session)
        )
        self.session_update_repository = (
            SqlAlchemySessionUpdateRepository(session)
        )
        self.session_read_repository = (
            SqlAlchemySessionReadRepository(session)
        )
        self.auth_read_repository = (
            SqlAlchemyAuthReadRepository(session)
        )
