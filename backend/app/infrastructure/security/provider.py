from app.domain.auth.actor_entity import Actor
from app.feature.auth.auth_exception import InvalidTokenError
from app.infrastructure.security.jwt import JoseJwt
from app.infrastructure.security.password_hasher import Argon2PasswordHasher
from app.infrastructure.security.refresh_token_generator import (
    RefreshTokenGenerator
)
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort
from app.shared.security.refresh_token_generator_port import (
    RefreshTokenGeneratorPort
)
from app.infrastructure.settings.provider import (
    get_jwt_algorithm,
    get_jwt_secret,
    get_jwt_issuer,
    get_access_token_ttl,
    get_token_hmac_secret,
)
from fastapi import Depends, HTTPException
from app.shared.security.token_hasher_port import TokenHasherPort
from app.infrastructure.security.token_hasher import HmacSha256TokenHasher
from functools import lru_cache
from app.feature.auth.auth_dependencies import oauth2_scheme


def get_refresh_token_generator() -> RefreshTokenGeneratorPort:
    return RefreshTokenGenerator()


def get_jwt(
    secret: str = Depends(get_jwt_secret),
    algorithm: str = Depends(get_jwt_algorithm),
    issuer: str = Depends(get_jwt_issuer),
    access_ttl_seconds: int = Depends(get_access_token_ttl)
) -> JwtPort:
    return JoseJwt(
        secret=secret,
        algorithm=algorithm,
        issuer=issuer,
        access_ttl_seconds=access_ttl_seconds
    )


@lru_cache
def get_token_hasher(
    secret: str = Depends(get_token_hmac_secret)
) -> TokenHasherPort:
    return HmacSha256TokenHasher(secret)


@lru_cache
def get_password_hasher() -> PasswordHasherPort:
    return Argon2PasswordHasher()


def get_current_actor(
    token: str = Depends(oauth2_scheme),
    jwt: JwtPort = Depends(get_jwt),
) -> Actor:
    try:
        return jwt.decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
