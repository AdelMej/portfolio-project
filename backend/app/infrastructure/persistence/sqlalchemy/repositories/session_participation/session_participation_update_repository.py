from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.session.session_exception import (
    NoActiveParticipationFoundError,
    SessionNotFoundError
)
from app.feature.stripe.repositories import (
    SessionParticipationUpdateRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


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

    async def cancel_registration(
        self,
        user_id: UUID,
        session_id: UUID
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.cancel_participation(
                    :user_id,
                    :session_id
                )
        """)

        try:
            await self._session.execute(stmt, {
                "user_id": user_id,
                "session_id": session_id
            })
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError()

            if code == "AP404":
                raise SessionNotFoundError()

            if code == "AB404":
                raise NoActiveParticipationFoundError()
