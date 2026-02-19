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


class SessionCancelledError(SessionDomainError):
    pass


class SessionAlreadyAttendedError(SessionDomainError):
    pass


class SessionAttendanceNotOpenError(SessionDomainError):
    pass


class InvalidAttendanceInputError(SessionDomainError):
    pass


class AlreadyActiveParticipationError(SessionDomainError):
    pass


class SessionIsFullError(SessionDomainError):
    pass


class SessionClosedForRegistration(SessionDomainError):
    pass


class OwnerCantRegisterToOwnSessionError(SessionDomainError):
    pass


class NoActiveParticipationFoundError(SessionDomainError):
    pass


class InvalidCoachAccountError(SessionDomainError):
    pass


class SessionNotFinishedError(SessionDomainError):
    pass
