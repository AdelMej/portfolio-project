from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.payment_intent.payment_intent_providers import PaymentProvider
from app.feature.stripe.repositories import (
    PaymentIntentUpdateRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


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
        provider_status: str,
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

    async def set_provider_id(
        self,
        user_id: UUID,
        session_id: UUID,
        provider: PaymentProvider,
        provider_intent_id: str
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.set_provider_id(
                    :user_id,
                    :session_id,
                    :provider,
                    :provider_intent_id
                )
        """)

        try:
            await self._session.execute(stmt, {
                "user_id": user_id,
                "session_id": session_id,
                "provider": provider,
                "provider_intent_id": provider_intent_id
            })

        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == 'AP404':
                return
