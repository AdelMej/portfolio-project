from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.coach.uow.coach_uow_port import (
    CoachUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyCoachStripeAccountReadRepo,
    SqlAlchemyCoachStripeAccountCreationRepo
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
