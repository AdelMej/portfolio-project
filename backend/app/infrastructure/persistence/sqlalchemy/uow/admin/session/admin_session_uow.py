from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.session.uow.admin_session_uow_port import (
    AdminSessionUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyAdminSessionReadRepo,
    SqlAlchemyAdminSessionUpdateRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyAdminSessionUoW(AdminSessionUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.session_read_repo = SqlAlchemyAdminSessionReadRepo(session)
        self.session_update_repo = SqlAlchemyAdminSessionUpdateRepo(session)

        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
