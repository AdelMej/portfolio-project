from typing import Protocol

from app.feature.coach.repositories import (
    CoachStripeAccountCreationRepoPort,
    CoachStripeAccountReadRepoPort,
    PaymentReadRepoPort,
    SessionReadRepoPort,
    PaymentCreationRepoPort
)


class CoachUoWPort(Protocol):
    coach_stripe_account_read_repo: CoachStripeAccountReadRepoPort
    coach_stripe_account_creation_repo: CoachStripeAccountCreationRepoPort
    payment_read_repo: PaymentReadRepoPort
    payment_creation_repo: PaymentCreationRepoPort
    session_read_repo: SessionReadRepoPort
