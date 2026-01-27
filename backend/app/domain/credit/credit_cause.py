from enum import Enum


class CreditCause(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    SESSION_USAGE = "session_usage"
    ADMIN_ADJUSTMENT = "admin_adjustment"
