from app.domain.user.user_exceptions import (
    FirstNameIsBlankError,
    FirstNameTooLongError,
    FirstNameTooShortError,
    LastNameIsBlankError,
    LastNameTooLongError,
    LastNameTooShortError,
)
from app.shared.utils.string_predicate import (
    is_blank
)
from app.shared.rules.user_profile_rules import (
    MIN_FIRST_NAME_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MIN_LAST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH
)


def ensure_first_name_is_valid(first_name: str):
    if is_blank(first_name):
        raise FirstNameIsBlankError()

    if len(first_name) < MIN_FIRST_NAME_LENGTH:
        raise FirstNameTooShortError()

    if len(first_name) > MAX_FIRST_NAME_LENGTH:
        raise FirstNameTooLongError()


def ensure_last_name_is_valid(last_name: str):
    if is_blank(last_name):
        raise LastNameIsBlankError()

    if len(last_name) < MIN_LAST_NAME_LENGTH:
        raise LastNameTooShortError()

    if len(last_name) > MAX_LAST_NAME_LENGTH:
        raise LastNameTooLongError()
