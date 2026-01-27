from app.shared.security.refresh_token_generator_port import (
    RefreshTokenGeneratorPort
)
import secrets


class RefreshTokenGenerator(RefreshTokenGeneratorPort):
    def generate(self) -> str:
        return secrets.token_urlsafe(64)
