from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepo,
)
from app.infrastructure.persistence.sqlalchemy.repositories.me import (
    SqlAlchemyMeReadRepo,
    SqlAlchemyMeUpdateRepo
)


class SqlAlchemyMeUoW(MeUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.me_read_repo = SqlAlchemyMeReadRepo(session)
        self.me_update_repo = SqlAlchemyMeUpdateRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
