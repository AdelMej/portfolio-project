from sqlalchemy import update
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from app.domain.auth.refresh_token_entity import NewRefreshTokenEntity
from app.feature.auth.repositories.auth_update_repository_port import (
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

    async def rotate_refresh_token(
        self,
        current_token_hash: str | None,
        new_token: NewRefreshTokenEntity
    ) -> None:

        # insert new refresh token
        res = await self._session.execute(
            text(
                """
                INSERT INTO app.refresh_tokens (
                    user_id,
                    token_hash,
                    expires_at
                )
                VALUES (
                    :user_id,
                    :token_hash,
                    :expires_at
                )
                RETURNING id
                """
            ),
            {
                "user_id": new_token.user_id,
                "token_hash": new_token.token_hash,
                "expires_at": new_token.expires_at
            }
        )
        new_id = res.scalar_one()

        # revoke and link old → new
        if current_token_hash:
            await self._session.execute(
                text(
                    """
                    UPDATE app.refresh_tokens
                    SET
                        replaced_by_token_id = :new_id
                        revoked_at = now()
                    WHERE token_hash = :old_hash
                        AND user_id = :user_id
                    """
                ),
                {
                    "new_id": new_id,
                    "old_hash": current_token_hash,
                    "user_id": new_token.user_id
                }
            )
