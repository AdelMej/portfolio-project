class SessionDomainError(Exception):
    pass


class SessionCreditNegativeError(SessionDomainError):
    pass


class SessionTimeIsInvalidError(SessionDomainError):
    pass


class SessionPriceIsNegativeError(SessionDomainError):
    pass


class SessionTitleIsBlankError(SessionDomainError):
    pass


class SessionTitleTooShortError(SessionDomainError):
    pass


class SessionTitleTooLongError(SessionDomainError):
    pass


class SessionOverlappingError(SessionDomainError):
    pass


class SessionNotFoundError(SessionDomainError):
    pass

class NotOwnerOfSessionError(SessionDomainError):
    pass
