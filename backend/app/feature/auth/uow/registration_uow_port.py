from typing import Protocol
from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepositoryPort
)


class RegistrationUoWPort(Protocol):
    auth_creation: AuthCreationRepositoryPort
