from typing import Protocol

from app.domain.payment_intent.payment_intent_entity import PaymentIntentEntity


class PaymentIntentReadRepoPort(Protocol):
    async def intent_exists(
        self,
        provider_payment_id: str
    ) -> bool:
        ...

    async def get_by_provider_id(
        self,
        provider_payment_id: str
    ) -> PaymentIntentEntity:
        ...
