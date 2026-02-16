from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.uow.session_public_uow_port import (
    SessionPulbicUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.session import (
    SqlAlchemySessionReadRepo
)


class SqlAlchemySessionPublicUoW(SessionPulbicUoWPort):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.session_read_repo = SqlAlchemySessionReadRepo(session)
