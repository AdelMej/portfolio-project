from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.domain.auth.actor_entity import Actor
from app.feature.admin.users.uow.admin_user_uow_port import AdminUserUoWPort
from app.feature.auth.uow.auth_uow_port import AuthUoWPort
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.infrastructure.persistence.sqlalchemy.UoW.admin import (
    SqlAlchemyAdminUserUoW
)
from app.infrastructure.persistence.sqlalchemy.UoW.auth import (
    SqlAlchemyMeUoW,
)
from app.infrastructure.persistence.sqlalchemy.UoW.auth.auth_uow import (
    SqlAlchemyAuthUoW
)
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.settings.provider import (
    get_app_system_session,
    get_app_user_session
)

from app.infrastructure.persistence.sqlalchemy.UoW.session.session_uow import SqlAlchemySessionUoW
from app.feature.session.session_uow_port import SessionUoWPort



async def get_auth_uow(
    session: AsyncSession = Depends(get_app_system_session)
) -> AuthUoWPort:
    return SqlAlchemyAuthUoW(session)


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


async def get_admin_user_uow(
        session: AsyncSession = Depends(get_app_user_session),
        actor: Actor = Depends(get_current_actor)
) -> AdminUserUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {"user_id": str(actor.id)},
    )
    return SqlAlchemyAdminUserUoW(session)
