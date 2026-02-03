from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.refresh_uow_port import (
    RefreshTokenUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepository,
    SqlAlchemyAuthUpdateRepository
)


class SqlalchemyRefreshTokenUoW(RefreshTokenUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.auth_read = SqlAlchemyAuthReadRepository(session)
        self.auth_update = SqlAlchemyAuthUpdateRepository(session)
