from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class UserProfileEntity:
    user_id: UUID
    first_name: str
    last_name: str


@dataclass(frozen=True)
class NewUserProfileEntity:
    first_name: str
    last_name: str
