from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.uow.session_public_uow_port import (
    SessionPulbicUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.session import (
    SqlAlchemySessionReadRepository
)


class SqlAlchemySessionPublicUoW(SessionPulbicUoWPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.session_read_repository = SqlAlchemySessionReadRepository(session)
