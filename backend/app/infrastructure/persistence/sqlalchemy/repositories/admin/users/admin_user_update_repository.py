from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.users.repositories import (
    AdminUserUpdateRepositoryPort
)


class SqlAlchemyAdminUserUpdateRepository(AdminUserUpdateRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def disable_user(
        self,
        user_id: UUID
    ) -> None:
        await self._session.execute(
            text("""
                UPDATE app.users
                SET
                    disabled_at = now(),
                    disabled_reason = 'admin'
                WHERE id = :user_id
                    AND disabled_at IS NULL
            """),
            {
                "user_id": str(user_id)
            }
        )

    async def reenable_user(
        self,
        user_id: UUID
    ) -> None:
        await self._session.execute(
            text("""
                UPDATE app.users
                SET
                    disabled_at = NULL,
                    disabled_reason = NULL
                WHERE id = :user_id
                    AND disabled_at IS NOT NULL
                    AND disabled_reason = 'admin'
            """),
            {
                "user_id": str(user_id)
            }
        )
