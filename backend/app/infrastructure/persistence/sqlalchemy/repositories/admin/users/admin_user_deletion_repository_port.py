from sqlalchemy.sql.expression import text
from app.feature.admin.users.repositories import (
    AdminUserDeletionRepositoryPort
)
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.role import Role


class SqlAlchemytAdminUserDeletionRepository(AdminUserDeletionRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def revoke_role(
        self,
        user_id: UUID,
        role: Role
    ) -> None:
        await self._session.execute(
            text("""
                DELETE FROM app.user_roles
                WHERE user_id = :user_id
                    AND role_id = (
                        SELECT id
                        FROM app.roles
                        WHERE role_name = :role_name
                    )
            """),
            {
                "user_id": str(user_id),
                "role_name": role
            }
        )
