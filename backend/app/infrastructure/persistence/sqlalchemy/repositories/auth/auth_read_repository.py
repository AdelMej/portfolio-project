from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.user.user_entity import UserEntity
from app.feature.auth.repositories.auth_read_repository import (
    AuthReadRepositoryPort
)
from app.infrastructure.persistence.sqlalchemy.models.users import User


class SqlAlchemyAuthReadRepository(AuthReadRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exist_email(self, email: str) -> bool:
        res = await self._session.execute(
            select(User.id).where(User.email == email)
        )
        return res.scalar_one_or_none() is not None

    async def get_user_by_email(self, email: str) -> UserEntity:
        res = await self._session.execute(
            select(User).where(User.email == email)
        )

        user = res.scalar_one()

        return UserEntity(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            disabled_at=user.disabled_at,
            disabled_reason=user.disabled_reason
        )
