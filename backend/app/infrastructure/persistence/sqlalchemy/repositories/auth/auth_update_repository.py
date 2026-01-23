from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.repositories.auth_update_repository import (
    AuthUpdateRepositoryPort
)
from app.shared.security.token_hasher_port import TokenHasherPort


class SqlAlchemyAuthUpdateRepository(AuthUpdateRepositoryPort):
    def __init__(
        self,
        session: AsyncSession,
        token_hasher: TokenHasherPort
    ) -> None:
        self._session = session
        self._token_hasher = token_hasher
