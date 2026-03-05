from typing import Protocol
from uuid import UUID

from app.domain.payment_intent.payment_intent_entity import PaymentIntentEntity
from app.domain.payment_intent.payment_intent_providers import PaymentProvider


class PaymentIntentReadRepoPort(Protocol):
    async def intent_exists(
        self,
        user_id: UUID,
        session_id: UUID,
        provider: PaymentProvider
    ) -> bool:
        ...

    async def get_by_identity(
        self,
        user_id: UUID,
        session_id: UUID,
        provider: PaymentProvider
    ) -> PaymentIntentEntity:
        ...
