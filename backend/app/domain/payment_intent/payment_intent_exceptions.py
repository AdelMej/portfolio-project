class PaymentIntentDomainError(Exception):
    pass


class PaymentInntentAlreadyExist(PaymentIntentDomainError):
    pass
