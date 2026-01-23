from app.infrastructure.security.refresh_token_generator import (
    RefreshTokenGenerator
)
from app.shared.security.refresh_token_geneartor_port import (
    RefreshTokenGeneratorPort
)


def get_refresh_token_generator() -> RefreshTokenGeneratorPort:
    return RefreshTokenGenerator()
