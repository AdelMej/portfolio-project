from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from app.domain.credit.credit_cause import CreditCause


@dataclass(frozen=True)
class CreditEntity():
    id: UUID
    user_id: UUID
    payment_id: UUID
    amount_cents: int
    currency: str
    balance_after_cents: int
    cause: CreditCause
    created_at: datetime


@dataclass(frozen=True)
class NewCreditEntity():
    user_id: UUID
    amount_cents: int
    currency: str
    cause: CreditCause
