from app.shared.security.password_hasher_port import PasswordHasherPort


class InMemoryPasswordHasher(PasswordHasherPort):
    def hash(self, plain: str) -> str:
        return plain

    def verify(self, plain: str, hashed: str) -> bool:
        return plain == hashed
