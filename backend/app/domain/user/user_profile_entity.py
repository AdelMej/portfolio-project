from dataclasses import dataclass


@dataclass(frozen=True)
class UserProfileEntity:
    first_name: str
    last_name: str
