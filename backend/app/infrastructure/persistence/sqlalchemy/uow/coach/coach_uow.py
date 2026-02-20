from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.coach.uow.coach_uow_port import (
    CoachUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyCoachStripeAccountReadRepo,
    SqlAlchemyCoachStripeAccountCreationRepo,
    SqlAlchemyPaymentReadRepo,
    SqlAlchemyPaymentCreationRepo,
    SqlAlchemySessionReadRepo,
    SqlAlchemyAuthReadRepo
)


class SqlAlchemyCoachUoW(CoachUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.coach_stripe_account_read_repo = (
            SqlAlchemyCoachStripeAccountReadRepo(session)
        )
        self.coach_stripe_account_creation_repo = (
            SqlAlchemyCoachStripeAccountCreationRepo(session)
        )
        self.payment_read_repo = (
            SqlAlchemyPaymentReadRepo(session)
        )
        self.payment_creation_repo = (
            SqlAlchemyPaymentCreationRepo(session)
        )
        self.session_read_repo = (
            SqlAlchemySessionReadRepo(session)
        )
        self.auth_read_repo = (
            SqlAlchemyAuthReadRepo(session)
        )
