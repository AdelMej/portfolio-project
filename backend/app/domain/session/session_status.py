from enum import Enum


class SessionStatus(str, Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
