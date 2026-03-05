from app.domain.auth.auth_exceptions import (
    EmailInvalidAtCountError,
    EmailInvalidDomainError,
    EmailInvalidLocalPartError,
    EmailIsBlankError,
    EmailLocalPartTooLongError,
    EmailSpaceError,
    EmailTooLongError,
    EmailTooShortError
)
from app.shared.rules.email_rules import (
    MAX_EMAIL_LENGTH,
    MAX_LOCAL_PART,
    MIN_EMAIL_LENGTH
)
from app.shared.utils.string_predicate import is_blank


def ensure_email_is_valid(email: str):
    if is_blank(email):
        raise EmailIsBlankError()

    if " " in email:
        raise EmailSpaceError()

    if len(email) < MIN_EMAIL_LENGTH:
        raise EmailTooShortError()

    if len(email) > MAX_EMAIL_LENGTH:
        raise EmailTooLongError()

    if email.count("@") != 1:
        raise EmailInvalidAtCountError()

    local, domain = email.split("@")

    if not local:
        raise EmailInvalidLocalPartError()

    if local.startswith(".") or local.endswith("."):
        raise EmailInvalidLocalPartError()

    if ".." in local:
        raise EmailInvalidLocalPartError()

    if len(local) > MAX_LOCAL_PART:
        raise EmailLocalPartTooLongError()

    if not domain or "." not in domain:
        raise EmailInvalidDomainError()

    if domain.startswith(".") or domain.endswith("."):
        raise EmailInvalidDomainError()
