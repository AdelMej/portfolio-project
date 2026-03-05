from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.expression import text
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.feature.admin.users.repositories import (
    AdminUserDeletionRepoPort
)
from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.role import Role
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemyAdminUserDeletionRepo(AdminUserDeletionRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def revoke_role(
        self,
        user_id: UUID,
        role: Role
    ) -> None:
        stmt = text("""
                SELECT
                    app_fcn.admin_user_revoke_role(:role_name, :user_id)
            """)
        try:
            await self._session.execute(stmt, {
                    "user_id": str(user_id),
                    "role_name": role
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            raise
