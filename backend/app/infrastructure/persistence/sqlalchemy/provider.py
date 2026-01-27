from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.auth.uow.login_uow import LoginUoWPort
from app.infrastructure.persistence.sqlalchemy.UoW.auth.login_uow import (
    SqlAlchemyLoginUoW
)
from app.infrastructure.settings.provider import get_app_system_session


async def get_login_uow(
    session: AsyncSession = Depends(get_app_system_session)
) -> LoginUoWPort:
    return SqlAlchemyLoginUoW(session)
