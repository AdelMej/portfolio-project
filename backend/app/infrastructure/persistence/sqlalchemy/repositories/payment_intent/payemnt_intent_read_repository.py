from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.payment_intent.payment_intent_entity import PaymentIntentEntity
from app.domain.payment_intent.payment_intent_providers import PaymentProvider
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
        user_id: UUID,
        session_id: UUID,
        provider: PaymentProvider
    ) -> bool:
        stmt = text("""
            SELECT
                app_fcn.intent_exists(
                    :user_id,
                    :session_id,
                    :provider
                )
        """)

        result = await self._session.execute(stmt, {
            "user_id": user_id,
            "session_id": session_id,
            "provider": provider
        })

        return result.scalar_one()

    async def get_by_identity(
        self,
        user_id: UUID,
        session_id: UUID,
        provider: PaymentProvider
    ) -> PaymentIntentEntity:
        stmt = text("""
            SELECT *
            FROM app_fcn.get_by_identity(
                    :user_id,
                    :session_id,
                    :provider
            )
        """)

        result = await self._session.execute(stmt, {
            "user_id": user_id,
            "session_id": session_id,
            "provider": provider
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
