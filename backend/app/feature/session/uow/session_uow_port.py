from typing import Protocol
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)
from app.feature.session.repositories import (
    PaymentIntentCreationRepoPort,
    SessionUpdateRepoPort,
    SessionCreationRepoPort,
    SessionReadRepoPort,
    CreditLedgerReadRepoPort,
    CreditLedgerCreationRepoPort,
    SessionParticipationCreationRepoPort,
    SessionAttendanceReadRepoPort,
    SessionAttendanceCreationRepoPort,
    SessionParticipationReadRepoPort,
    SessionParticipationUpdateRepoPort,
    CoachStripeAccountReadRepoPort
)


class SessionUoWPort(Protocol):
    session_creation_repo: SessionCreationRepoPort
    session_update_repo: SessionUpdateRepoPort
    session_read_repo: SessionReadRepoPort
    session_participation_read_repo: SessionParticipationReadRepoPort
    session_participation_creation_repo: SessionParticipationCreationRepoPort
    session_participation_update_repo: SessionParticipationUpdateRepoPort
    session_attendance_read_repo: SessionAttendanceReadRepoPort
    session_attendance_creation_repo: SessionAttendanceCreationRepoPort
    payment_intent_creation_repo: PaymentIntentCreationRepoPort
    credit_ledger_read_repo: CreditLedgerReadRepoPort
    credit_ledger_creation_repo: CreditLedgerCreationRepoPort
    auth_read_repo: AuthReadRepoPort
    coach_stripe_account_read_repo: CoachStripeAccountReadRepoPort
