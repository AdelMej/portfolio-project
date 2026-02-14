from enum import Enum


class PaymentProvier(str, Enum):
    STRIPE = 'stripe'
