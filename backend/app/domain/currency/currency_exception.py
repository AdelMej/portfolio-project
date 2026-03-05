class CurrencyDomainException(Exception):
    pass


class CurrencyInvalidLengthError(CurrencyDomainException):
    pass


class CurrencyInvalidFormatError(CurrencyDomainException):
    pass
