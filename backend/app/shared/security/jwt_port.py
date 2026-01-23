from typing import Protocol
from uuid import UUID
from app.domain.auth.actor_entity import Actor


class JwtPort(Protocol):
    def issue_access_token(
        self,
        *,
        user_id: UUID,
    ) -> str: ...

    def issue_refresh_token(
        self,
        *,
        user_id: UUID,
        token_id: UUID,
    ) -> str: ...

    def decode_access_token(self, token: str) -> Actor: ...
