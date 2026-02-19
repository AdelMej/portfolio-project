import json
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.session.session_exception import (
    InvalidAttendanceInputError,
    SessionAttendanceNotOpenError,
    SessionCancelledError,
    SessionNotFoundError
)
from app.feature.session.repositories import (
    SessionAttendanceCreationRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemySessionAttendanceCreationRepo(
    SessionAttendanceCreationRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_attendance(
        self,
        session_id: UUID,
        attendance_list: dict[UUID, bool]
    ) -> None:
        payload = [
            {
                "user_id": str(user_id),
                "attended": attended
            }
            for user_id, attended in attendance_list.items()
        ]

        stmt = text("""
            SELECT app_fcn.create_attendance(
                :session_id,
                :attendance_list
            )
            """)

        try:
            await self._session.execute(stmt, {
                    "session_id": session_id,
                    "attendance_list": json.dumps(payload)
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            if code == "AP404":
                raise SessionNotFoundError() from exc

            if code == "AP409":
                raise SessionCancelledError() from exc

            if code == "AB409":
                raise SessionAttendanceNotOpenError() from exc

            if code == "AP422":
                raise InvalidAttendanceInputError() from exc

            raise
