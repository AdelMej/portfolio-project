from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyMeReadRepository
)


class SqlAlchemyMeUoW(MeUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.me_read_repository = SqlAlchemyMeReadRepository(session)
