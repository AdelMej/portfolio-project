from app.domain.auth.auth_exceptions import (
    RefreshTokenIsBlankError,
    RefreshTokenTooShortError,
    RefreshTokenTooLongError
)
from app.shared.rules.refresh_token_rules import (
    REFRESH_TOKEN_MAX_SIZE,
    REFRESH_TOKEN_MIN_SIZE
)
from app.shared.utils.string_predicate import is_blank


def ensure_refresh_token_is_valid(refresh_token: str) -> None:
    if is_blank(refresh_token):
        raise RefreshTokenIsBlankError()

    if len(refresh_token) < REFRESH_TOKEN_MIN_SIZE:
        raise RefreshTokenTooShortError()

    if len(refresh_token) > REFRESH_TOKEN_MAX_SIZE:
        raise RefreshTokenTooLongError()
