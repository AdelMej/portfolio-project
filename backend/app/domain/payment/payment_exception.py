class PaymentDomainException(Exception):
    pass


class PaymentProviderError(PaymentDomainException):
    pass
