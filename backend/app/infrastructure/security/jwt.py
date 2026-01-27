from datetime import datetime, timedelta, timezone
from uuid import UUID
from app.domain.auth.actor_entity import Actor, TokenActor
from app.domain.auth.permission import ROLE_PERMISSIONS, Permission
from app.domain.auth.role import Role
from app.shared.security.jwt_port import JwtPort
from jose import jwt, JWTError
from app.feature.auth.auth_exception import InvalidTokenError


class JoseJwt(JwtPort):
    def __init__(
        self,
        *,
        secret: str,
        algorithm: str,
        issuer: str,
        access_ttl_seconds: int,
    ):
        self._secret = secret
        self._algorithm = algorithm
        self._issuer = issuer
        self._access_ttl = timedelta(seconds=access_ttl_seconds)

    def issue_access_token(self, *, actor: TokenActor) -> str:
        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(actor.id),
            "role": [r.value for r in actor.roles],
            "iss": self._issuer,
            "iat": now,
            "exp": now + self._access_ttl
        }

        return jwt.encode(
            payload,
            self._secret,
            algorithm=self._algorithm
        )

    def decode_access_token(self, token: str) -> Actor:
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[self._algorithm],
                issuer=self._issuer,
            )
        except JWTError as exc:
            raise InvalidTokenError() from exc

        permissions: set[Permission] = set()
        for r in payload["roles"]:
            permissions |= ROLE_PERMISSIONS[Role(r)]

        return Actor(
            id=UUID(payload["sub"]),
            type=payload["role"],
            permissions=frozenset(permissions),
        )
