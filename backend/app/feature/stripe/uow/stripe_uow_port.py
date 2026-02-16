from app.feature.stripe.repositories import (
    PaymentIntentReadRepoPort,
    PaymentIntentUpdateRepoPort,
    SessionParticipationUpdateRepoPort,
    PaymentCreationRepoPort
)


class StripeUoWPort():
    payment_intent_read_repo: PaymentIntentReadRepoPort
    payment_intent_update_repo: PaymentIntentUpdateRepoPort
    session_participation_update_repo: SessionParticipationUpdateRepoPort
    payment_creation_repo: PaymentCreationRepoPort
