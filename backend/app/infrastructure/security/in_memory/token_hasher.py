from app.shared.security.token_hasher_port import TokenHasherPort


class InMemoryTokenHasher(TokenHasherPort):
    def hash(self, raw: str) -> str:
        return raw

    def verify(self, raw: str, hashed: str) -> bool:
        return raw == hashed
