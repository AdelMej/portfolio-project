from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.session.session_exception import SessionOverlappingError
from app.feature.session.repositories.session_update_repository_port import (
    SessionUpdateRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemySessionUpdateRepo(SessionUpdateRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_session(
        self,
        session_id: UUID,
        title: str,
        starts_at: datetime,
        ends_at: datetime
    ) -> None:
        stmt = text("""
                SELECT
                    app_fcn.session_update(
                        :session_id,
                        :title,
                        :starts_at,
                        :ends_at
                    )
            """)

        try:
            await self._session.execute(stmt, {
                    "session_id": session_id,
                    "title": title,
                    "starts_at": starts_at,
                    "ends_at": ends_at
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            if code == "AP409":
                raise SessionOverlappingError() from exc

            raise

    async def cancel_session(
            self,
            session_id: UUID
    ) -> bool:
        ...
