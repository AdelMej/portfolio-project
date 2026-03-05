from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.session.uow.session_uow_port import (
    SessionUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemySessionParticipationReadRepo,
    SqlAlchemySessionParticipationCreationRepo,
    SqlAlchemySessionParticipationUpdateRepo,
    SqlAlchemySessionUpdateRepo,
    SqlAlchemySessionReadRepo,
    SqlAlchemySessionCreationRepo,
    SqlAlchemyAuthReadRepo,
    SqlAlchemySessionAttendanceReadRepo,
    SqlAlchemySessionAttendanceCreationRepo,
    SqlAlchemyPaymentIntentCreationRepo,
    SqlAlchemyCreditLedgerReadRepo,
    SqlAlchemyCreditLedgerCreationRepo,
    SqlAlchemyCoachStripeAccountReadRepo
)


class SqlAlchemySessionUoW(SessionUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.session_creation_repo = SqlAlchemySessionCreationRepo(session)
        self.session_update_repo = SqlAlchemySessionUpdateRepo(session)
        self.session_read_repo = SqlAlchemySessionReadRepo(session)
        self.session_participation_read_repo = (
            SqlAlchemySessionParticipationReadRepo(session)
        )
        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
        self.session_participation_creation_repo = (
            SqlAlchemySessionParticipationCreationRepo(session)
        )
        self.session_attendance_read_repo = (
            SqlAlchemySessionAttendanceReadRepo(session)
        )
        self.session_attendance_creation_repo = (
            SqlAlchemySessionAttendanceCreationRepo(session)
        )
        self.payment_intent_creation_repo = (
            SqlAlchemyPaymentIntentCreationRepo(session)
        )
        self.credit_ledger_read_repo = (
            SqlAlchemyCreditLedgerReadRepo(session)
        )
        self.credit_ledger_creation_repo = (
            SqlAlchemyCreditLedgerCreationRepo(session)
        )
        self.session_participation_update_repo = (
            SqlAlchemySessionParticipationUpdateRepo(session)
        )
        self.coach_stripe_account_read_repo = (
            SqlAlchemyCoachStripeAccountReadRepo(session)
        )
