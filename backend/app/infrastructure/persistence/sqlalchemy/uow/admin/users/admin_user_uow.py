from app.feature.admin.users.uow.admin_user_uow_port import (
    AdminUserUoWPort
)
from sqlalchemy.ext.asyncio.session import AsyncSession


from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlalchemyAdminUserReadRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyAdminUserUoW(AdminUserUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.admin_user_read_repo = SqlalchemyAdminUserReadRepo(session)
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
