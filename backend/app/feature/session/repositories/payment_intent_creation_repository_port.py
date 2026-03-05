from typing import Protocol

from app.domain.payment_intent.payment_intent_entity import (
    NewPaymentIntentEntity
)


class PaymentIntentCreationRepoPort(Protocol):
    async def create_payment_intent(
        self,
        payment_intent: NewPaymentIntentEntity,
    ) -> None:
        ...
