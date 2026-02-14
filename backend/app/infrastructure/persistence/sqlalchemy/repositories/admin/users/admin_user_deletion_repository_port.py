from sqlalchemy.sql.expression import text
from app.feature.admin.users.repositories import (
    AdminUserDeletionRepoPort
)
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.role import Role


class SqlAlchemyAdminUserDeletionRepo(AdminUserDeletionRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def revoke_role(
        self,
        user_id: UUID,
        role: Role
    ) -> None:
        await self._session.execute(
            text("""
                SELECT
                    app_fcn.admin_user_revoke_role(:role_name, :user_id)
            """),
            {
                "user_id": str(user_id),
                "role_name": role
            }
        )
