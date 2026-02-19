class StripeDomainError(Exception):
    pass


class IntentIsInvalidError(StripeDomainError):
    pass


class ChargeNotReadyError(StripeDomainError):
    pass


class BalanceNotExpendedError(StripeDomainError):
    pass


class AccountIsInvalid(StripeDomainError):
    pass


class CoachPayoutFailedError(StripeDomainError):
    pass
