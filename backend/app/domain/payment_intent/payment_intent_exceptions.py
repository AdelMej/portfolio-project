class PaymentIntentDomainError(Exception):
    pass


class PaymentIntentAlreadyExist(PaymentIntentDomainError):
    pass
