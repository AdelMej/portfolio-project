from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from app.domain.user.user_profile_entity import AdminUserAttendanceRead
from app.feature.admin.session.repositories import (
    AdminSessionAttendanceReadRepoPort
)


class SqlAlchemyAdminSessionAttendanceReadRepo(
    AdminSessionAttendanceReadRepoPort
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

    async def get_session_attendance_list(
        self,
        session_id: UUID
    ) -> list[AdminUserAttendanceRead]:
        stmt = text("""
            SELECT *
            FROM app_fcn.fetch_attendance_list(:session_id)
        """)

        res = await self._session.execute(stmt, {
            "session_id": session_id
        })

        rows = res.mappings().all()

        return [
            AdminUserAttendanceRead(
                user_id=row["user_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                attended=row["attended"]
            )for row in rows
        ]
