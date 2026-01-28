from app.shared.security.password_hasher_port import PasswordHasherPort
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Argon2PasswordHasher(PasswordHasherPort):
    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    def hash(self, plain: str) -> str:
        return self._hasher.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        try:
            return self._hasher.verify(plain, hashed)
        except VerifyMismatchError:
            return False
