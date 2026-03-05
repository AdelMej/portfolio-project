class CreditDomainError(Exception):
    pass


class InvalidCreditAmount(CreditDomainError):
    pass


class CreditNegativeError(CreditDomainError):
    pass
