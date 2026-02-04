from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.users.repositories import (
    AdminUserUpdateRepositoryPort
)


class SqlAlchemyAdminUserUpdateRepository(AdminUserUpdateRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
