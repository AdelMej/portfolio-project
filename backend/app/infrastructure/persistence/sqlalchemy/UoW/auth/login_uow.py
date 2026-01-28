from app.feature.auth.uow.login_uow_port import LoginUoWPort
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthUpdateRepository,
    SqlAlchemyAuthReadRepository,
    SqlAlchemyAuthCreationRepository
)


class SqlAlchemyLoginUoW(LoginUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.auth_read = SqlAlchemyAuthReadRepository(session)
        self.auth_update = SqlAlchemyAuthUpdateRepository(session)
        self.auth_creation = SqlAlchemyAuthCreationRepository(session)
