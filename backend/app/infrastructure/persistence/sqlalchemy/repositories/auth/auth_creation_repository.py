from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.refresh_token_entity import NewRefreshTokenEntity
from app.feature.auth.repositories.auth_creation_respository_port import (
    AuthCreationRepositoryPort
)
from app.infrastructure.persistence.sqlalchemy.models.refresh_tokens import (
    RefreshToken
)


class SqlAlchemyAuthCreationRepository(AuthCreationRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_refresh_token(self, token: NewRefreshTokenEntity) -> None:
        new_token = RefreshToken(
            user_id=token.user_id,
            token_hash=token.token_hash,
            expires_at=token.expires_at
        )

        self._session.add(new_token)
