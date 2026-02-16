from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.me_system_uow_port import (
    MeSystemUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepo,
)
from app.infrastructure.persistence.sqlalchemy.repositories.me import (
    SqlAlchemyMeDeleteRepo,
    SqlAlchemyMeUpdateRepo
)


class SqlAlchemyMeSystemUoW(MeSystemUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.me_update_repo = SqlAlchemyMeUpdateRepo(session)
        self.me_delete_repo = SqlAlchemyMeDeleteRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
