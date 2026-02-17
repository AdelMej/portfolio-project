from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.stripe.repositories import (
    SessionParticipationUpdateRepoPort
)


class SqlAlchemySessionParticipationUpdateRepo(
    SessionParticipationUpdateRepoPort
):
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        self._session = session

    async def user_paid(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.mark_participation_paid(
                    :session_id,
                    :user_id
                )
        """)

        await self._session.execute(stmt, {
            "session_id": session_id,
            "user_id": user_id
        })

    async def cancel_unpaid(
        self,
        session_id: UUID,
        user_id: UUID
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.cancel_unpaid_participation(
                    :session_id,
                    :user_id
                )
        """)

        await self._session.execute(stmt, {
            "session_id": session_id,
            "user_id": user_id
        })
