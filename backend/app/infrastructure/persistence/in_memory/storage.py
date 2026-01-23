from uuid import UUID
from app.domain.user.user_entity import User
from app.domain.auth.refresh_token_entity import RefreshToken


class InMemoryAuthStorage:
    def __init__(self) -> None:
        self.users: dict[UUID, User] = {}
        self.users_by_email: dict[str, UUID] = {}
        self.refresh_tokens: dict[UUID, RefreshToken] = {}
