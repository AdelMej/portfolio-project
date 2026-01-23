from uuid import UUID
from app.domain.user.user_entity import UserEntity
from app.domain.auth.refresh_token_entity import RefreshTokenEntity


class InMemoryAuthStorage:
    def __init__(self) -> None:
        self.users: dict[UUID, UserEntity] = {}
        self.users_by_email: dict[str, UUID] = {}
        self.refresh_tokens: dict[str, RefreshTokenEntity] = {}
