from datetime import datetime
from app.domain.session.session_exception import (
    SessionCreditNegativeError,
    SessionPriceIsNegativeError,
    SessionTimeIsInvalidError,
    SessionTitleIsBlankError,
    SessionTitleTooLongError,
    SessionTitleTooShortError
)
from app.shared.utils.string_predicate import (
    is_blank
)
from app.shared.rules.session_title_rules import (
    MAX_TITLE_LENGTH,
    MIN_TITLE_LENGTH
)


def ensure_price_is_not_negative(price: int):
    if price < 0:
        raise SessionPriceIsNegativeError()


def ensure_times_valid(starts_at: datetime, end_at: datetime):
    if end_at <= starts_at:
        raise SessionTimeIsInvalidError()


def ensure_credit_non_negative(credit: int):
    if credit < 0:
        raise SessionCreditNegativeError()


def ensure_title_is_valid(title: str):
    if is_blank(title):
        raise SessionTitleIsBlankError()

    if len(title) < MIN_TITLE_LENGTH:
        raise SessionTitleTooShortError()

    if len(title) > MAX_TITLE_LENGTH:
        raise SessionTitleTooLongError()
