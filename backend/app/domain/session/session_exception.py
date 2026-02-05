class SessionAlreadyCancelledError(Exception):
    pass

class SessionDomainError(Exception):
    """Base domain error for session logic."""
    pass

class SessionCreditNegativeError(SessionDomainError):
    """Raised when session credit is negative."""
    pass