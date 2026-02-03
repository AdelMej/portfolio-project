from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.refresh_token_entity import RefreshTokenEntity
from app.domain.auth.role import Role
from app.domain.user.user_entity import UserEntity
from app.feature.auth.repositories.auth_read_repository_port import (
    AuthReadRepositoryPort
)


class SqlAlchemyAuthReadRepository(AuthReadRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exist_email(self, email: str) -> bool:
        stmt = text("""
            SELECT 1
            FROM app.users
            WHERE email = :email
            LIMIT 1
        """)

        res = await self._session.execute(stmt, {"email": email})
        return res.scalar() is not None

    async def get_user_by_email(self, email: str) -> UserEntity | None:
        stmt = text("""
            SELECT
                u.id,
                u.email,
                u.password_hash,
                u.disabled_at,
                u.disabled_reason,
                array_agg(r.role_name) as roles
            FROM app.users u
            JOIN app.user_roles ur ON ur.user_id = u.id
            JOIN app.roles r ON r.id = ur.role_id
            where u.email = :email
            GROUP BY
                u.id,
                u.email,
                u.password_hash,
                u.disabled_at,
                u.disabled_reason
            """)

        res = await self._session.execute(stmt, {"email": email})
        row = res.mappings().one_or_none()

        if row is None:
            return None

        roles = {Role(r) for r in row["roles"]}

        return UserEntity(
            id=row["id"],
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
                FROM app.refresh_tokens
                WHERE token_hash = :token_hash
                  AND revoked_at IS NULL
            """),
            {"token_hash": token_hash}
        )

        row = res.mappings().one_or_none()
        if not row:
            return None

        return RefreshTokenEntity(**row)

    async def get_user_by_id(
            self,
            user_id: UUID
    ) -> UserEntity | None:
        stmt = text("""
            SELECT
                u.id,
                u.email,
                u.password_hash,
                u.disabled_at,
                u.disabled_reason,
                array_agg(r.role_name) as roles
            FROM app.users u
            JOIN app.user_roles ur ON ur.user_id = u.id
            JOIN app.roles r ON r.id = ur.role_id
            where u.id = :user_id
            GROUP BY
                u.id,
                u.email,
                u.password_hash,
                u.disabled_at,
                u.disabled_reason
            """)

        res = await self._session.execute(stmt, {"user_id": user_id})
        row = res.mappings().one_or_none()

        if row is None:
            return None

        roles = {Role(r) for r in row["roles"]}

        return UserEntity(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            roles=roles,
            disabled_at=row["disabled_at"],
            disabled_reason=row["disabled_reason"]
        )
