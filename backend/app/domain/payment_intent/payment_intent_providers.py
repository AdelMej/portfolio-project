from enum import Enum


class PaymentProvider(str, Enum):
    STRIPE = 'stripe'
