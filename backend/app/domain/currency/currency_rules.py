from app.domain.currency.currency_exception import (
    CurrencyInvalidFormatError,
    CurrencyInvalidLengthError
)
from app.shared.rules.currency_rules import (
    CURRENCY_LENGTH
)
from app.shared.utils.string_predicate import (
    is_alpha_ascii,
)


def ensure_currency_is_valid(currency: str):
    if len(currency) != CURRENCY_LENGTH:
        raise CurrencyInvalidLengthError()

    if not is_alpha_ascii(currency):
        raise CurrencyInvalidFormatError()
