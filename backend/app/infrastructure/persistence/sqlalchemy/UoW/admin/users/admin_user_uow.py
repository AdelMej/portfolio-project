from app.feature.admin.users.uow.admin_user_uow_port import (
    AdminUserUoWPort
)
from sqlalchemy.ext.asyncio.session import AsyncSession


from app.infrastructure.persistence.sqlalchemy.repositories.admin import (
    SqlalchemyAdminUserReadRepository,
)


class SqlAlchemyAdminUserUoW(AdminUserUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.admin_user_read_repository = (
            SqlalchemyAdminUserReadRepository(session)
        )
