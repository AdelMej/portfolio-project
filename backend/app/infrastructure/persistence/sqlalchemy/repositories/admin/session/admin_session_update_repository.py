from uuid import UUID
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.session.session_exception import (
    SessionNotFoundError,
    SessionStartedError
)
from app.feature.admin.session.repositories import (
    AdminSessionUpdateRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemyAdminSessionUpdateRepo(
    AdminSessionUpdateRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def cancel_session(
            self,
            session_id: UUID
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.cancel_session(:session_id)
        """)

        try:
            await self._session.execute(stmt, {
                "session_id": session_id
            })
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError()

            if code == "AP404":
                raise SessionNotFoundError()

            if code == "AP409":
                raise SessionStartedError()

            raise
