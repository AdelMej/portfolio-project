from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.feature.admin.users.repositories import (
    AdminUserUpdateRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemyAdminUserUpdateRepo(AdminUserUpdateRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def disable_user(
        self,
        user_id: UUID
    ) -> None:
        stmt = text("""
                SELECT
                    app_fcn.admin_user_disable_user(:user_id)
            """)

        try:
            await self._session.execute(stmt, {"user_id": str(user_id)})
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError()

            raise

    async def reenable_user(
        self,
        user_id: UUID
    ) -> None:
        stmt = text("""
                SELECT
                    app_fcn.admin_user_enable_user(:user_id)
            """)
        try:
            await self._session.execute(stmt, {"user_id": str(user_id)})
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            raise
