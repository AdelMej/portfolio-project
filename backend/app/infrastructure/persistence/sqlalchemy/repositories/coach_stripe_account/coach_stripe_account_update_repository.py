from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.feature.stripe.repositories import (
    CoachStripeAccountUpdateRepoPort
)


class SqlAlchemyCoachStripeAccountUpdateRepo(
    CoachStripeAccountUpdateRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_by_account_id(
        self,
        account_id: str,
        details_submitted: bool,
        charges_enabled: bool,
        payouts_enabled: bool
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.update_by_stripe_account_id(
                    :account_id,
                    :details_submitted,
                    :charges_enabled,
                    :payouts_enabled
                )
        """)

        await self._session.execute(stmt, {
            "account_id": account_id,
            "details_submitted": details_submitted,
            "charges_enabled": charges_enabled,
            "payouts_enabled": payouts_enabled
        })
