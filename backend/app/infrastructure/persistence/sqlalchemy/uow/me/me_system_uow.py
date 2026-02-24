from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.me.uow.me_system_uow_port import (
    MeSystemUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyMeDeleteRepo,
    SqlAlchemyMeUpdateRepo,
    SqlAlchemyAuthUpdateRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyMeSystemUoW(MeSystemUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.me_update_repo = SqlAlchemyMeUpdateRepo(session)
        self.me_delete_repo = SqlAlchemyMeDeleteRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
        self.auth_update_repo = SqlAlchemyAuthUpdateRepo(session)
