from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.domain.auth.role import Role
from app.feature.admin.users.repositories import (
    AdminUserCreationRepositoryPort
)


class SqlAlchemyAdminUserCreationRepository(AdminUserCreationRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def grant_role(
        self,
        user_id: UUID,
        role: Role,
    ) -> None:

        await self._session.execute(
            text("""
                SELECT
                 app_fcn.admin_user_grant_role(:role_name, :user_id)
            """),
            {
                "user_id": str(user_id),
                "role_name": role
            }
        )
