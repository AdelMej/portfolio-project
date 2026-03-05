from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.me.uow.me_uow_port import MeUoWPort
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyMeReadRepo,
    SqlAlchemyMeUpdateRepo,
    SqlAlchemyAuthReadRepo,
    SqlAlchemySessionReadRepo
)


class SqlAlchemyMeUoW(MeUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.me_read_repo = SqlAlchemyMeReadRepo(session)
        self.me_update_repo = SqlAlchemyMeUpdateRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
        self.session_read_repo = SqlAlchemySessionReadRepo(session)
