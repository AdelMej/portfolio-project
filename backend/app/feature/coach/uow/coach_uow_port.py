from typing import Protocol

from app.feature.coach.repositories import (
    CoachStripeAccountCreationRepoPort,
    CoachStripeAccountReadRepoPort,
)


class CoachUoWPort(Protocol):
    coach_stripe_account_read_repo: CoachStripeAccountReadRepoPort
    coach_stripe_account_creation_repo: CoachStripeAccountCreationRepoPort
