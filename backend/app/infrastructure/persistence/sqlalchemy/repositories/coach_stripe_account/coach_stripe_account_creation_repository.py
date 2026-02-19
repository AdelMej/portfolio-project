from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.coach.repositories import (
    CoachStripeAccountCreationRepoPort
)


class SqlAlchemyCoachStripeAccountCreationRepo(
    CoachStripeAccountCreationRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_account(
        self,
        stripe_acount_id: str
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.create_coach_stripe_account(
                    :stripe_acount_id
                )
        """)

        await self._session.execute(stmt, {
            "stripe_acount_id": stripe_acount_id
        })
