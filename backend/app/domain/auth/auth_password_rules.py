
from zxcvbn import zxcvbn
from app.domain.auth.auth_exceptions import (
    PasswordIsBlankError,
    PasswordMissingDigitError,
    PasswordMissingLowercaseError,
    PasswordMissingSpecialCharError,
    PasswordMissingUppercaseError,
    PasswordTooLongError,
    PasswordTooShortError,
    PasswordTooWeakError
)
from app.shared.rules.password_rules import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    MIN_ZXCVBN_SCORE
)
from app.shared.utils.string_predicate import (
    contains_digit,
    contains_lowercase,
    contains_special,
    contains_uppercase,
    is_blank
)


def ensure_password_is_strong(password: str):
    if is_blank(password):
        raise PasswordIsBlankError()

    if len(password) < MIN_PASSWORD_LENGTH:
        raise PasswordTooShortError()

    if len(password) > MAX_PASSWORD_LENGTH:
        raise PasswordTooLongError()

    if not contains_lowercase(password):
        raise PasswordMissingLowercaseError()

    if not contains_uppercase(password):
        raise PasswordMissingUppercaseError()

    if not contains_digit(password):
        raise PasswordMissingDigitError()

    if not contains_special(password):
        raise PasswordMissingSpecialCharError()

    result = zxcvbn(password)

    if result["score"] < MIN_ZXCVBN_SCORE:
        raise PasswordTooWeakError()
