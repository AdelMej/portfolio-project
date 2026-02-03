class UserDomainError(Exception):
    pass


class FirstNameIsBlankError(UserDomainError):
    pass


class FirstNameTooShortError(UserDomainError):
    pass


class FirstNameTooLongError(UserDomainError):
    pass


class LastNameIsBlankError(UserDomainError):
    pass


class LastNameTooShortError(UserDomainError):
    pass


class LastNameTooLongError(UserDomainError):
    pass
