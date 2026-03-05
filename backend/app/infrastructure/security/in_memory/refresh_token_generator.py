from app.shared.security.token_generator_port import (
    RefreshTokenGeneratorPort
)
import secrets


class InMemoryRefreshTokenGenerator(RefreshTokenGeneratorPort):
    def generate(self) -> str:
        return secrets.token_urlsafe(64)
