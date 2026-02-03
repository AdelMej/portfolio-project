from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.logout_uow_port import (
    LogoutUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthUpdateRepository
)


class SqlAlchemyLogoutUoW(LogoutUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.auth_update = SqlAlchemyAuthUpdateRepository(session)
