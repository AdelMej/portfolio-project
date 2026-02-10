from enum import Enum


class CreditCause(str, Enum):
    SESSION_CANCELLED = "session_cancelled"
    SESSION_USAGE = "session_usage"
    ADMIN_ADJUSTMENT = "admin_adjustment"
