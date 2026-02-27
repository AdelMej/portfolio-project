from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class PaymentIntentEntity:
    id: UUID
    user_id: UUID
    session_id: UUID
    provider: str
    provider_intent_id: str
    status: str
    credit_applied_cents: int
    amount_cents: int
    currency: str


@dataclass(frozen=True)
class NewPaymentIntentEntity:
    user_id: UUID
    session_id: UUID
    provider: str
    provider_intent_id: str | None
    status: str
    credit_applied_cents: int
    amount_cents: int
    currency: str
