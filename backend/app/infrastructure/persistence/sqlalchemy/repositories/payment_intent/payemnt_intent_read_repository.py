from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.payment_intent.payment_intent_entity import PaymentIntentEntity
from app.feature.stripe.repositories import (
    PaymentIntentReadRepoPort
)


class SqlAlchemyPaymentIntentReadRepo(
    PaymentIntentReadRepoPort
):
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        self._session = session

    async def intent_exists(
        self,
        provider_payment_id: str
    ) -> bool:
        stmt = text("""
            SELECT
                app_fcn.intent_exists(:provider_payment_id)
        """)

        result = await self._session.execute(stmt, {
            "provider_payment_id": provider_payment_id
        })

        return result.scalar_one()

    async def get_by_provider_id(
        self,
        provider_payment_id: str
    ) -> PaymentIntentEntity:
        stmt = text("""
            SELECT *
            FROM app_fcn.get_by_provider_id(
                    :provider_payment_id
            )
        """)

        result = await self._session.execute(stmt, {
            "provider_payment_id": provider_payment_id
        })

        row = result.mappings().one()

        return PaymentIntentEntity(
            id=row["id"],
            user_id=row["user_id"],
            session_id=row["session_id"],
            provider=row["provider"],
            provider_intent_id=row["provider_intent_id"],
            status=row["status"],
            credit_applied_cents=row["credit_applied_cents"],
            amount_cents=row["amount_cents"],
            currency=row["currency"]
        )
