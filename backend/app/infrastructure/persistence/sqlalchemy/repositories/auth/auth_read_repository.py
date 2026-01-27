from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.domain.auth.refresh_token_entity import RefreshTokenEntity
from app.domain.auth.role import Role
from app.domain.user.user_entity import UserEntity
from app.feature.auth.repositories.auth_read_repository import (
    AuthReadRepositoryPort
)
from app.infrastructure.persistence.sqlalchemy.models.refresh_tokens import (
    RefreshToken
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

        roles = {Role(r.name) for r in user.roles}

        return UserEntity(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            roles=roles,
            disabled_at=user.disabled_at,
            disabled_reason=user.disabled_reason
        )

    async def get_refresh_token(
            self,
            token_hash: str
    ) -> RefreshTokenEntity | None:
        res = await self._session.execute(
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None)
            )
        )

        token = res.scalar_one_or_none()

        if not token:
            return None

        return RefreshTokenEntity(
            user_id=token.user_id,
            token_hash=token.token_hash,
            created_at=token.created_at,
            expires_at=token.expires_at,
            revoked_at=token.revoked_at,
        )
