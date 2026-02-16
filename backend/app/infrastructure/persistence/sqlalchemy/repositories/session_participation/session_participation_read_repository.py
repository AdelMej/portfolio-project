from uuid import UUID

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.feature.session.repositories import (
    SessionParticipationReadRepoPort
)


class SqlAlchemySessionParticipationReadRepo(SessionParticipationReadRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def has_active_participation(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.has_active_participation(
                        :user_id,
                        :session_id
                    )
            """),
            {
                "user_id": user_id,
                "session_id": session_id
            }
        )

        return result.scalar_one()

    async def is_session_full(
        self,
        session_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.is_session_full(:session_id, 6)
            """),
            {
                "session_id": session_id
            }
        )

        return result.scalar_one()

    async def is_registration_open(
        self,
        session_id: UUID
    ) -> bool:
        result = await self._session.execute(
            text("""
                SELECT
                    app_fcn.is_registration_open(:session_id)
            """),
            {
                "session_id": session_id
            }
        )

        return result.scalar_one()
