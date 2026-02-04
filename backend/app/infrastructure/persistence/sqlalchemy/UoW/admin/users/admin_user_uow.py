from app.feature.admin.users.uow.admin_user_uow_port import (
    AdminUserUoWPort
)
from sqlalchemy.ext.asyncio.session import AsyncSession


from app.infrastructure.persistence.sqlalchemy.repositories.admin import (
    SqlalchemyAdminUserReadRepository,
    SqlAlchemyAdminUserUpdateRepository,
    SqlAlchemyAdminUserCreationRepository,
    SqlAlchemytAdminUserDeletionRepository
)


class SqlAlchemyAdminUserUoW(AdminUserUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.admin_user_read_repository = (
            SqlalchemyAdminUserReadRepository(session)
        )
        self.admin_user_update_repository = (
            SqlAlchemyAdminUserUpdateRepository(session)
        )
        self.admin_user_creation_repository = (
            SqlAlchemyAdminUserCreationRepository(session)
        )
        self.admin_user_deletion_repository = (
            SqlAlchemytAdminUserDeletionRepository(session)
        )
