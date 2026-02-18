from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.coach.repositories import (
    CoachStripeAccountReadRepoPort
)


class SqlAlchemyCoachStripeAccountReadRepo(
    CoachStripeAccountReadRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def account_exists(
        self,
        coach_id: UUID
    ) -> bool:
        stmt = text("""
            SELECT
                app_fcn.stripe_account_exists(
                    :coach_id
                )
        """)

        res = await self._session.execute(stmt, {
            "coach_id": coach_id
        })

        return res.scalar_one()

    async def get_account_id(
        self,
        coach_id: UUID
    ) -> str | None:
        stmt = text("""
            SELECT
                app_fcn.get_stripe_account_id(
                    :coach_id
                )
        """)

        res = await self._session.execute(stmt, {
            "coach_id": coach_id
        })

        return res.scalar_one()
