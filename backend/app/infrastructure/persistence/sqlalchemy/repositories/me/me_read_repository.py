from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.domain.auth.role import Role
from app.domain.user.user_entity import UserEntity
from app.domain.user.user_profile_entity import UserProfileEntity
from app.feature.auth.repositories.me_read_repository_port import (
    MeReadRepoPort
)


class SqlAlchemyMeReadRepo(MeReadRepoPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: UUID) -> UserEntity:
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

        res = await self._session.execute(
            stmt,
            {"user_id": str(user_id)}
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

    async def get_profile_by_id(self, user_id: UUID) -> UserProfileEntity:
        res = await self._session.execute(
            text("""
            SELECT user_id, first_name, last_name
            FROM app.user_profiles
            WHERE user_id = :user_id
            """),
            {
                "user_id": user_id
            }
        )

        row = res.mappings().one()

        return UserProfileEntity(
            user_id=row["user_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
        )
