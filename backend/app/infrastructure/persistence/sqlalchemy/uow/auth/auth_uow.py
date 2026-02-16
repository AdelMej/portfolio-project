from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.auth_uow_port import AuthUoWPort
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthUpdateRepo,
    SqlAlchemyAuthReadRepo,
    SqlAlchemyAuthCreationRepo
)


class SqlAlchemyAuthUoW(AuthUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.auth_update_repo = SqlAlchemyAuthUpdateRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
        self.auth_creation_repo = SqlAlchemyAuthCreationRepo(session)
