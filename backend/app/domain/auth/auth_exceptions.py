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


class ExpiredRefreshTokenError(AuthDomainError):
    pass


class InvalidRefreshTokenError(AuthDomainError):
    pass


class RevokedRefreshTokenError(AuthDomainError):
    pass


class RefreshTokenIsBlankError(AuthDomainError):
    pass


class RefreshTokenTooShortError(AuthDomainError):
    pass


class RefreshTokenTooLongError(AuthDomainError):
    pass


class EmailAlreadyExistError(AuthDomainError):
    pass


class EmailIsBlankError(AuthDomainError):
    pass


class EmailTooShortError(AuthDomainError):
    pass


class EmailTooLongError(AuthDomainError):
    pass


class EmailInvalidAtCountError(AuthDomainError):
    pass


class EmailInvalidLocalPartError(AuthDomainError):
    pass


class EmailLocalPartTooLongError(AuthDomainError):
    pass


class EmailInvalidDomainError(AuthDomainError):
    pass


class EmailSpaceError(AuthDomainError):
    pass


class PasswordIsBlankError(AuthDomainError):
    pass


class PasswordTooShortError(AuthDomainError):
    pass


class PasswordTooLongError(AuthDomainError):
    pass


class PasswordMissingLowercaseError(AuthDomainError):
    pass


class PasswordMissingUppercaseError(AuthDomainError):
    pass


class PasswordMissingDigitError(AuthDomainError):
    pass


class PasswordMissingSpecialCharError(AuthDomainError):
    pass


class PasswordTooWeakError(AuthDomainError):
    pass


class PasswordMissmatchError(AuthDomainError):
    pass


class PasswordReuseError(AuthDomainError):
    pass


class AdminCantSelfDeleteError(AuthDomainError):
    pass


class AdminCantSelfRevokeError(AuthDomainError):
    pass


class BaseRoleCannotBeRevokedError(AuthDomainError):
    pass


class AdminCantSelfDisableError(AuthDomainError):
    pass


class AdminCantSelfRennableError(AuthDomainError):
    pass
