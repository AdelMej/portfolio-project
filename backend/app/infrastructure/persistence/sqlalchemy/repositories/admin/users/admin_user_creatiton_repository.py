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
                INSERT INTO app.user_roles(user_id, role_id)
                SELECT
                    :user_id,
                    r.id
                FROM app.roles r
                WHERE role_name = :role_name
                ON CONFLICT DO NOTHING;
            """),
            {
                "user_id": str(user_id),
                "role_name": role
            }
        )
