from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.stripe.repositories import (
    PaymentIntentUpdateRepoPort
)


class SqlAlchemyPaymentIntentUpdateRepo(
    PaymentIntentUpdateRepoPort
):
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        self._session = session

    async def mark_payment_intent(
        self,
        provider_payment_id: str,
        provider_status: str
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.mark_payment_intent(
                    :provider_payment_id,
                    :provider_status
                )
        """)

        await self._session.execute(stmt, {
            "provider_payment_id": provider_payment_id,
            "provider_status": provider_status
        })
