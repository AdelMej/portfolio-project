from app.infrastructure.security.in_memory.jwt import (
    InMemoryJwt,
)
from app.infrastructure.security.in_memory.password_hasher import (
    InMemoryPasswordHasher
)
from app.infrastructure.security.in_memory.token_hasher import (
    InMemoryTokenHasher
)
from app.infrastructure.security.in_memory.refresh_token_generator import (
    InMemoryRefreshTokenGenerator
)
from app.shared.security.jwt_port import JwtPort
from app.shared.security.password_hasher_port import PasswordHasherPort
from app.shared.security.token_generator_port import (
    RefreshTokenGeneratorPort
)
from app.shared.security.token_hasher_port import TokenHasherPort


def get_in_memory_jwt() -> JwtPort:
    return InMemoryJwt()


def get_in_memory_password_hasher() -> PasswordHasherPort:
    return InMemoryPasswordHasher()


def get_in_memory_token_hasher() -> TokenHasherPort:
    return InMemoryTokenHasher()


def get_in_memory_refresh_token_generator() -> RefreshTokenGeneratorPort:
    return InMemoryRefreshTokenGenerator()
