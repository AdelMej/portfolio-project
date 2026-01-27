from typing import Protocol
from app.domain.auth.actor_entity import Actor, TokenActor


class JwtPort(Protocol):
    def issue_access_token(
        self,
        *,
        actor: TokenActor,
    ) -> str: ...

    def decode_access_token(self, token: str) -> Actor: ...
