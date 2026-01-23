# infra/security/in_memory/jwt.py
from uuid import UUID
from app.shared.security.jwt_port import JwtPort
from app.domain.auth.actor_entity import Actor


class InMemoryJwt(JwtPort):
    def issue_access_token(self, *, user_id: UUID) -> str:
        return f"access:{user_id}"

    def issue_refresh_token(self, *, user_id: UUID, token_id: UUID) -> str:
        return f"refresh:{token_id}"

    def decode_access_token(self, token: str) -> Actor:
        prefix, raw_id = token.split(":")
        if prefix != "access":
            raise ValueError("Invalid token type")

        return Actor(
            id=UUID(raw_id),
            type="user",
            permissions=frozenset(),
        )
