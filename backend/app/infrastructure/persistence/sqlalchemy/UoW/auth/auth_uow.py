from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.auth_uow_port import AuthUoWPort
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthUpdateRepository,
    SqlAlchemyAuthReadRepository,
    SqlAlchemyAuthCreationRepository
)


class SqlAlchemyAuthUoW(AuthUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.auth_update_repository = SqlAlchemyAuthUpdateRepository(session)
        self.auth_read_repository = SqlAlchemyAuthReadRepository(session)
        self.auth_creation_repository = (
                SqlAlchemyAuthCreationRepository(session)
        )
