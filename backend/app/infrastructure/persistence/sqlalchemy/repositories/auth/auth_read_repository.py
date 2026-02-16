from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.refresh_token_entity import RefreshTokenEntity
from app.domain.auth.role import Role
from app.domain.user.user_entity import UserEntity
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepoPort
)


class SqlAlchemyAuthReadRepo(AuthReadRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exist_email(self, email: str) -> bool:
        res = await self._session.execute(
            text("""
                SELECT app_fcn.auth_exists_by_email(:email)
            """),
            {
                "email": email
            }
        )
        exists = res.scalar_one()
        return exists

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        res = await self._session.execute(
            text("""
                SELECT *
                FROM app_fcn.auth_user_by_email(:email)
            """),
            {
                "email": email
            }
        )
        row = res.mappings().one_or_none()

        if row is None:
            return None

        roles = {Role(r) for r in row["roles"]}

        return UserEntity(
            id=row["user_id"],
            email=row["email"],
            password_hash=row["password_hash"],
            roles=roles,
            disabled_at=row["disabled_at"],
            disabled_reason=row["disabled_reason"]
        )

    async def get_refresh_token(
        self,
        token_hash: str
    ) -> RefreshTokenEntity | None:
        res = await self._session.execute(
            text("""
                SELECT
                    user_id,
                    token_hash,
                    created_at,
                    expires_at,
                    revoked_at
                FROM app_fcn.get_active_refresh_token(:token_hash)
            """),
            {
                "token_hash": token_hash
            }
        )

        row = res.mappings().one_or_none()
        if not row:
            return None

        return RefreshTokenEntity(**row)

    async def get_user_by_id(
            self,
            user_id: UUID
    ) -> UserEntity:

        res = await self._session.execute(
            text("""
            SELECT *
                FROM app_fcn.auth_user_by_id(:user_id)
            """),
            {
                "user_id": user_id
            }
        )
        row = res.mappings().one()

        roles = {Role(r) for r in row["roles"]}

        return UserEntity(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            roles=roles,
            disabled_at=row["disabled_at"],
            disabled_reason=row["disabled_reason"]
        )

    async def is_user_disabled(
        self,
        user_id: UUID
    ) -> bool:
        res = await self._session.execute(
            text("""
                SELECT EXISTS(
                    SELECT 1
                    FROM app.users
                    WHERE id = :user_id
                        AND disabled_at IS NOT NULL
                )
            """),
            {
                "user_id": str(user_id)
            }
        )

        return res.scalar_one()
