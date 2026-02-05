from uuid import UUID
from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.repositories.me_delete_repository_port import (
    MeDeleteRepositoryPort
)
from app.shared.utils.time import utcnow


class SqlAlchemyMeDeleteRepository(MeDeleteRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def soft_delete_user(
            self,
            user_id: UUID,
            new_password_hash: str
    ) -> None:
        email = 'deleted+'+str(user_id)+'@deleted.actual.com'

        await self._session.execute(
            text("""
                UPDATE app.user_profiles
                SET
                    first_name = :first_name,
                    last_name = :last_name
                WHERE user_id = :user_id
            """),
            {
                "first_name": "deleted",
                "last_name": "deleted",
                "user_id": user_id
            }
        )

        await self._session.execute(
            text("""
                UPDATE app.users
                SET
                    email = :email,
                    password_hash = :password_hash,
                    disabled_at = :disabled_at,
                    disabled_reason = :disabled_reason
                WHERE id = :user_id
            """),
            {
                "email": email,
                "password_hash": new_password_hash,
                "disabled_at": utcnow(),
                "disabled_reason": "self",
                "user_id": user_id
            }
        )
