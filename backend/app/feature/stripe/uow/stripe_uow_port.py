from app.feature.stripe.repositories import (
    PaymentIntentReadRepoPort,
    PaymentIntentUpdateRepoPort,
    SessionParticipationUpdateRepoPort,
    PaymentCreationRepoPort,
    CreditLedgerCreationRepoPort,
    CoachStripeAccountUpdateRepoPort
)


class StripeUoWPort():
    payment_intent_read_repo: PaymentIntentReadRepoPort
    payment_intent_update_repo: PaymentIntentUpdateRepoPort
    session_participation_update_repo: SessionParticipationUpdateRepoPort
    payment_creation_repo: PaymentCreationRepoPort
    credit_ledger_creation_repo: CreditLedgerCreationRepoPort
    coach_stripe_account_update_repo: CoachStripeAccountUpdateRepoPort
