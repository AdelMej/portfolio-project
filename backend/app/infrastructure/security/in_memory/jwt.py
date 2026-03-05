# infra/security/in_memory/jwt.py
from uuid import UUID
from app.shared.security.jwt_port import JwtPort
from app.domain.auth.actor_entity import Actor, TokenActor


class InMemoryJwt(JwtPort):
    def issue_access_token(self, *, actor: TokenActor) -> str:
        return f"access:{actor.id}"

    def decode_access_token(self, token: str) -> Actor:
        prefix, raw_id = token.split(":")
        if prefix != "access":
            raise ValueError("Invalid token type")

        return Actor(
            id=UUID(raw_id),
            type="user",
            permissions=frozenset(),
        )
