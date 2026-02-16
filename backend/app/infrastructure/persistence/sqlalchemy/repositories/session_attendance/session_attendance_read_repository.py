import json
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.session.session_exception import InvalidAttendanceInputError
from app.domain.user.user_profile_entity import UserProfileEntity
from app.feature.session.repositories import (
    SessionAttendanceReadRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemySessionAttendanceReadRepo(
    SessionAttendanceReadRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def is_session_attended(
        self,
        session_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.is_session_attended(
                        :session_id
                    )
            """),
            {
                "session_id": session_id
            }
        )

        return result.scalar_one()

    async def get_attendance(
        self,
        session_id: UUID
    ) -> list[UserProfileEntity]:
        stmt = text(
                """
                SELECT
                    app_fcn.get_pre_attendance(:session_id)
                """
            )
        try:
            result = await self._session.execute(stmt, {
                    "session_id": session_id
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            raise

        rows = result.mappings().all()

        return [
            UserProfileEntity(
                user_id=row["user_id"],
                first_name=row["first_name"],
                last_name=row["last_name"]
            ) for row in rows
        ]

    async def is_session_attendance_open(
        self,
        session_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.is_attendance_open(:session_id)
            """),
            {
                "session_id": session_id
            }
        )

        return result.scalar_one()

    async def is_attendance_payload_valid(
        self,
        session_id: UUID,
        attendance_list: dict[UUID, bool]
    ) -> bool:
        payload = [
            {
                "user_id": str(uid), "attended": attended
            } for uid, attended in attendance_list.items()
        ]

        stmt = text("""
                SELECT
                    app_fcn.is_attendance_payload_valid(
                        :session_id,
                        :attendance_list
                    )
            """)
        try:
            result = await self._session.execute(stmt, {
                    "session_id": session_id,
                    "attendance_list": json.dumps(payload)
                }
            )
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            if code == "AP422":
                raise InvalidAttendanceInputError() from exc

            raise

        return result.scalar_one()
