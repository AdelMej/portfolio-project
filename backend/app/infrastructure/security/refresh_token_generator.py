from app.shared.security.token_generator_port import (
    TokenGeneratorPort
)
import secrets


class TokenGenerator(TokenGeneratorPort):
    def generate(self) -> str:
        return secrets.token_urlsafe(64)
