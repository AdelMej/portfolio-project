from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.payment.payment_entity import NewPaymentEntity
from app.feature.stripe.repositories import (
    PaymentCreationRepoPort
)


class SqlAlchemyPaymentCreationRepo(PaymentCreationRepoPort):
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        self._session = session

    async def create_payment(
        self,
        new_payment: NewPaymentEntity
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.create_payment(
                    :session_id,
                    :user_id,
                    :provider,
                    :provider_payment_id,
                    :gross_amount_cents,
                    :provider_fee_cents,
                    :net_amount_cents,
                    :currency
                )
        """)

        await self._session.execute(stmt, {
            "session_id": new_payment.session_id,
            "user_id": new_payment.user_id,
            "provider": new_payment.provider,
            "provider_payment_id": new_payment.provider_payment_id,
            "gross_amount_cents": new_payment.gross_amount_cents,
            "provider_fee_cents": new_payment.provider_fee_cents,
            "net_amount_cents": new_payment.net_amount_cents,
            "currency": new_payment.currency
        })
