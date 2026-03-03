from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.session_participation.session_participation_entity import (
    NewSessionParticipationEntity
)
from app.domain.session.session_exception import (
    AlreadyActiveParticipationError,
    SessionCancelledError,
    SessionIsFullError,
    SessionNotFoundError
)
from app.feature.session.repositories import (
    SessionParticipationCreationRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemySessionParticipationCreationRepo(
    SessionParticipationCreationRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_participation(
        self,
        participation: NewSessionParticipationEntity,
        expires_at: datetime
    ) -> None:
        stmt = text("""
                SELECT
                    app_fcn.create_session_participation(
                        :user_id,
                        :session_id,
                        :expires_at
                    )
            """)

        try:
            await self._session.execute(stmt, {
                "user_id": participation.user_id,
                "session_id": participation.session_id,
                "expires_at": expires_at
            })
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            if code == "AP404":
                raise SessionNotFoundError() from exc

            if code == "AP410":
                raise SessionCancelledError() from exc

            if code == "AP409":
                raise AlreadyActiveParticipationError() from exc

            if code == "AB409":
                raise SessionIsFullError() from exc

            raise
