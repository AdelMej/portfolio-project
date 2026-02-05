from datetime import datetime
from app.domain.session.session_exception import SessionCreditNegativeError, SessionDomainError

def ensure_price_is_not_negative(price: int):
    if price < 0:
        raise SessionDomainError("Price cannot be negative")

def ensure_times_valid(starts_at: datetime, end_at: datetime):
    if end_at <= starts_at:
        raise SessionDomainError("End time must be after start time")

def ensure_credit_non_negative(credit: int):
    if credit < 0:
        raise SessionCreditNegativeError("Session credit cannot be negative")
