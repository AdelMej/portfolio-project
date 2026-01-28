class AuthDomainError(Exception):
    pass


class InvalidEmailError(AuthDomainError):
    pass


class InvalidPasswordError(AuthDomainError):
    pass


class UserDisabledError(AuthDomainError):
    pass


class RefreshTokenNotFoundError(AuthDomainError):
    pass


class PermissionDeniedError(AuthDomainError):
    pass
