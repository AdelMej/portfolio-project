from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyMeReadRepository,
    SqlAlchemyMeUpdateRepository,
    SqlAlchemyAuthReadRepository
)


class SqlAlchemyMeUoW(MeUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.me_read_repository = SqlAlchemyMeReadRepository(session)
        self.me_update_repository = SqlAlchemyMeUpdateRepository(session)
        self.auth_read_repository = SqlAlchemyAuthReadRepository(session)
