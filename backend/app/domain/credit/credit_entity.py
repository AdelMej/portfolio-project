from dataclasses import dataclass
from datetime import datetime
from app.domain.credit.credit_cause import CreditCause


@dataclass(frozen=True)
class CreditEntity():
    amount_cents: int
    balance_after_cents: int
    cause: CreditCause
    created_at: datetime
