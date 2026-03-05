import hmac
import hashlib
from app.shared.security.token_hasher_port import TokenHasherPort


class HmacSha256TokenHasher(TokenHasherPort):
    def __init__(self, secret: str):
        self._secret = secret.encode()

    def hash(self, raw: str) -> str:
        return hmac.new(
            self._secret,
            raw.encode(),
            hashlib.sha256,
        ).hexdigest()

    def verify(self, raw: str, hashed: str) -> bool:
        expected = self.hash(raw)
        return hmac.compare_digest(expected, hashed)
