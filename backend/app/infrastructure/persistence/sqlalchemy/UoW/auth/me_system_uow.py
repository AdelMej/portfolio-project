from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.me_system_uow_port import (
    MeSystemUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepository,
    SqlAlchemyMeUpdateRepository,
    SqlAlchemyMeDeleteRepository
)


class SqlAlchemyMeSystemUoW(MeSystemUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.me_update_repository = SqlAlchemyMeUpdateRepository(session)
        self.me_delete_repository = SqlAlchemyMeDeleteRepository(session)
        self.auth_read_repository = SqlAlchemyAuthReadRepository(session)
