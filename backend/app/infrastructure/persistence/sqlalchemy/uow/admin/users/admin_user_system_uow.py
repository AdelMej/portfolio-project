from app.feature.admin.users.uow.admin_user_system_uow_port import (
    AdminUserSystemUoWPort
)
from sqlalchemy.ext.asyncio.session import AsyncSession


from app.infrastructure.persistence.sqlalchemy.repositories.admin import (
    SqlAlchemyAdminUserUpdateRepo,
    SqlAlchemyAdminUserCreationRepo,
    SqlAlchemyAdminUserDeletionRepo
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyAdminUserSystemUoW(AdminUserSystemUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.admin_user_update_repo = SqlAlchemyAdminUserUpdateRepo(session)
        self.admin_user_creation_repo = SqlAlchemyAdminUserCreationRepo(
            session
        )
        self.admin_user_deletion_repo = SqlAlchemyAdminUserDeletionRepo(
            session
        )
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
