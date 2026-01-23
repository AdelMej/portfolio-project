class AuthDomainError(Exception):
    pass


class InvalidEmailError(AuthDomainError):
    pass


class InvalidPasswordError(AuthDomainError):
    pass


class InvalidCredentialsError(AuthDomainError):
    pass


class UserDisabledError(AuthDomainError):
    pass
