from app.feature.admin.users.uow.admin_user_system_uow_port import (
    AdminUserSystemUoWPort
)
from sqlalchemy.ext.asyncio.session import AsyncSession


from app.infrastructure.persistence.sqlalchemy.repositories.admin import (
    SqlAlchemyAdminUserUpdateRepository,
    SqlAlchemyAdminUserCreationRepository,
    SqlAlchemyAdminUserDeletionRepository
)
from app.infrastructure.persistence.sqlalchemy.repositories.auth import (
    SqlAlchemyAuthReadRepository
)


class SqlAlchemyAdminUserSystemUoW(AdminUserSystemUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.admin_user_update_repository = (
            SqlAlchemyAdminUserUpdateRepository(session)
        )
        self.admin_user_creation_repository = (
            SqlAlchemyAdminUserCreationRepository(session)
        )
        self.admin_user_deletion_repository = (
            SqlAlchemyAdminUserDeletionRepository(session)
        )
        self.auth_read_repository = (
            SqlAlchemyAuthReadRepository(session)
        )
