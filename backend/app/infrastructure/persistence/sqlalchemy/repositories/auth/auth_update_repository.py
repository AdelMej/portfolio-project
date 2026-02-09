from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import text
from app.domain.auth.refresh_token_entity import NewRefreshTokenEntity
from app.feature.auth.repositories.auth_update_repository_port import (
    AuthUpdateRepositoryPort
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
            text(
                """
                UPDATE app.refresh_tokens
                SET revoked_at = now()
                WHERE token_hash = :token_hash
                """
            ),
            {"token_hash": token_hash}
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
                    SELECT
                        app_fcn.create_refresh_token(
                            :user_id,
                            :token_hash,
                            :expires_at
                        )
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
                        SELECT
                            app_fcn.rotate_refresh_token(
                                :new_id,
                                :old_hash,
                                :user_id
                            )
                    """
                ),
                {
                    "new_id": new_id,
                    "old_hash": current_token_hash,
                    "user_id": new_token.user_id
                }
            )

    async def revoke_all_refresh_token(self, user_id: UUID) -> None:
        await self._session.execute(
            text("""
            UPDATE app.refresh_tokens
            SET
                revoked_at = :revoked_at
            WHERE user_id = :user_id
                AND revoked_at IS NULL
            """),
            {
                "revoked_at": utcnow(),
                "user_id": user_id
            }
        )
