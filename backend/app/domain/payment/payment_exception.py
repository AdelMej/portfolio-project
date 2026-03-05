class PaymentDomainException(Exception):
    pass


class PaymentProviderError(PaymentDomainException):
    pass


class PaymentAlreadyPaidError(PaymentDomainException):
    pass
