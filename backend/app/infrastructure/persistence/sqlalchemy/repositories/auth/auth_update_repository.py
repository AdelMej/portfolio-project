from sqlalchemy import update
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.repositories.auth_update_repository import (
    AuthUpdateRepositoryPort
)
from app.infrastructure.persistence.sqlalchemy.models.refresh_tokens import (
    RefreshToken
)
from app.shared.utils.time import utcnow


class SqlAlchemyAuthUpdateRepository(AuthUpdateRepositoryPort):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def revoke_refresh_token(self, token_hash: str) -> None:
        await self._session.execute(
            update(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.token_hash.is_(None),
            )
            .values(revoked_at=utcnow())
        )
