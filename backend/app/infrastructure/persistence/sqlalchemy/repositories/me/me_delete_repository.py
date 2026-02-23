from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.me.repositories.me_delete_repository_port import (
    MeDeleteRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate
from app.domain.auth.auth_exceptions import (
    PermissionDeniedError
)


class SqlAlchemyMeDeleteRepo(MeDeleteRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def soft_delete_user(
            self,
            user_id: UUID,
    ) -> None:
        stmt = text("""
                SELECT
                    app_fcn.me_self_delete(:user_id)
            """)

        try:
            await self._session.execute(stmt, {"user_id": user_id})
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == 'AP401':
                raise PermissionDeniedError() from exc

            raise
