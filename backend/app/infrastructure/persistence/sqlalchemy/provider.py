from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.domain.auth.actor_entity import Actor
from app.feature.auth.uow.login_uow_port import LoginUoWPort
from app.feature.auth.uow.logout_uow_port import LogoutUoWPort
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.feature.auth.uow.refresh_uow_port import RefreshTokenUoWPort
from app.feature.auth.uow.registration_uow_port import RegistrationUoWPort
from app.infrastructure.persistence.sqlalchemy.UoW.auth import (
    SqlAlchemyMeUoW,
    SqlAlchemyLoginUoW,
    SqlalchemyRefreshTokenUoW,
    SqlAlchemyLogoutUoW
)
from app.infrastructure.persistence.sqlalchemy.UoW.auth.registration_uow import SqlAlchemyRegistrationUoW
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.settings.provider import (
    get_app_system_session,
    get_app_user_session
)

from app.infrastructure.persistence.sqlalchemy.UoW.session.session_uow import SqlAlchemySessionUoW
from app.feature.session.session_uow_port import SessionUoWPort



async def get_login_uow(
    session: AsyncSession = Depends(get_app_system_session)
) -> LoginUoWPort:
    return SqlAlchemyLoginUoW(session)


async def get_me_uow(
    session: AsyncSession = Depends(get_app_user_session),
    actor: Actor = Depends(get_current_actor)
) -> MeUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {"user_id": str(actor.id)},
    )
    return SqlAlchemyMeUoW(session)

async def get_session_uow(
    actor: Actor = Depends(get_current_actor),
    session: AsyncSession = Depends(get_app_user_session)
) -> SessionUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {"user_id": str(actor.id)},)
    return SqlAlchemySessionUoW(session)


async def get_refresh_uow(
        session: AsyncSession = Depends(get_app_system_session)
) -> RefreshTokenUoWPort:
    return SqlalchemyRefreshTokenUoW(session)


async def get_logout_uow(
        session: AsyncSession = Depends(get_app_system_session)
) -> LogoutUoWPort:
    return SqlAlchemyLogoutUoW(session)


async def get_registration_uow(
        session: AsyncSession = Depends(get_app_system_session)
) -> RegistrationUoWPort:
    return SqlAlchemyRegistrationUoW(session)

