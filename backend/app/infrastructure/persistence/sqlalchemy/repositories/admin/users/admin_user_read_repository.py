from app.domain.auth.role import Role
from app.domain.user.user_entity import AdminUserRead
from app.feature.admin.users.repositories import (
    AdminUserReadRepositoryPort
)
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession


class SqlalchemyAdminUserRead(AdminUserReadRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all_users(
        self,
        offset: int,
        limit: int
    ) -> tuple[list[AdminUserRead], bool]:

        res = await self._session.execute(
            text("""
                SELECT
                    u.id,
                    u.email,
                    u.disabled_at,
                    u.created_at,
                    COALESCE(
                        array_agg(DISTINCT r.role_name ORDER by r.role_name),
                        '{}'
                    ) AS roles
                FROM app.users u
                LEFT JOIN app.user_roles ur on  ur.user_id = u.id
                LEFT JOIN app.roles r on ur.role_id = r.id
                GROUP BY
                    u.id,
                    u.email,
                    u.disabled_at,
                    u.created_at
                ORDER BY u.created_at DESC
                OFFSET :offset
                LIMIT :limit_plus_one
            """),
            {
                "offset": offset,
                "limit_plus_one": limit + 1
            }
        )

        rows = res.mappings().all()
        has_more = len(rows) > limit
        rows = rows[:limit]

        return [
            AdminUserRead(
                id=row["id"],
                email=row["email"],
                roles={Role(role) for role in row["roles"]},
                disabled_at=row["disabled_at"],
                created_at=row["created_at"],
            ) for row in rows
        ], has_more
