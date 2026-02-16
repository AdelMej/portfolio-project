from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.auth_exceptions import PermissionDeniedError
from app.domain.payment_intent.payment_intent_entity import (
    NewPaymentIntentEntity
)
from app.domain.payment_intent.payment_intent_exceptions import (
    PaymentInntentAlreadyExist
)
from app.domain.session.session_exception import SessionNotFoundError
from app.feature.session.repositories import (
    PaymentIntentCreationRepoPort
)
from app.shared.database.sqlstate_extractor import get_sqlstate


class SqlAlchemyPaymentIntentCreationRepo(
    PaymentIntentCreationRepoPort
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_payment_intent(
        self,
        payment_intent: NewPaymentIntentEntity
    ) -> None:
        stmt = text("""
            SELECT
                app_fcn.create_payment_intent(
                    :user_id,
                    :session_id,
                    :provider,
                    :provider_intent_id,
                    :status,
                    :amount_cents,
                    :credit_applied,
                    :currency
                )
        """)

        try:
            await self._session.execute(stmt, {
                "user_id": payment_intent.user_id,
                "session_id": payment_intent.session_id,
                "provider": payment_intent.provider,
                "provider_intent_id": payment_intent.provider_intent_id,
                "status": payment_intent.status,
                "amount_cents": payment_intent.amount_cents,
                "credit_applied": payment_intent.credit_applied_cents,
                "currency": payment_intent.currency
            })
        except DBAPIError as exc:
            code = get_sqlstate(exc)

            if code == "AP401":
                raise PermissionDeniedError() from exc

            if code == "AP404":
                raise SessionNotFoundError() from exc

            if code == "AP409":
                raise PaymentInntentAlreadyExist() from exc

            raise
