from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.stripe.uow.stripe_uow_port import (
    StripeUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyPaymentIntentReadRepo,
    SqlAlchemyPaymentIntentUpdateRepo,
    SqlAlchemySessionParticipationUpdateRepo,
    SqlAlchemyPaymentCreationRepo,
    SqlAlchemyCreditLedgerCreationRepo,
    SqlAlchemyCoachStripeAccountUpdateRepo
)


class SqlAlchemyStripeUoW(StripeUoWPort):
    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        self._session = session

        self.payment_intent_read_repo = (
            SqlAlchemyPaymentIntentReadRepo(session)
        )
        self.payment_intent_update_repo = (
            SqlAlchemyPaymentIntentUpdateRepo(session)
        )
        self.session_participation_update_repo = (
            SqlAlchemySessionParticipationUpdateRepo(session)
        )
        self.payment_creation_repo = SqlAlchemyPaymentCreationRepo(session)
        self.credit_ledger_creation_repo = (
            SqlAlchemyCreditLedgerCreationRepo(session)
        )
        self.coach_stripe_account_update_repo = (
            SqlAlchemyCoachStripeAccountUpdateRepo(session)
        )
