from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import text
from app.domain.auth.actor_entity import Actor
from app.feature.admin.users.uow.admin_user_system_uow_port import (
    AdminUserSystemUoWPort
)
from app.feature.admin.users.uow.admin_user_uow_port import AdminUserUoWPort
from app.feature.auth.uow.auth_uow_port import AuthUoWPort
from app.feature.auth.uow.me_system_uow_port import MeSystemUoWPort
from app.feature.auth.uow.me_uow_port import MeUoWPort
from app.feature.credit.uow.credit_uow_port import CreditUoWPort
from app.feature.payment.uow.payment_uow_port import PaymentUoWPort
from app.feature.session.uow.session_public_uow_port import (
    SessionPulbicUoWPort
)
from app.infrastructure.persistence.sqlalchemy.uow.admin import (
    SqlAlchemyAdminUserUoW,
    SqlAlchemyAdminUserSystemUoW
)
from app.infrastructure.persistence.sqlalchemy.uow.auth import (
    SqlAlchemyMeUoW,
)
from app.infrastructure.persistence.sqlalchemy.uow.auth.auth_uow import (
    SqlAlchemyAuthUoW
)
from app.infrastructure.persistence.sqlalchemy.uow.auth.me_system_uow import (
    SqlAlchemyMeSystemUoW
)
from app.infrastructure.persistence.sqlalchemy.uow.credit.credit_uow import (
    SqlAlchemyCreditUoW
)
from app.infrastructure.persistence.sqlalchemy.uow.payment.payment_uow import (
    SqlAlchemyPaymenUoW
)
from app.infrastructure.persistence.sqlalchemy.uow.session import (
    SqlAlchemySessionPublicUoW,
    SqlAlchemySessionUoW
)
from app.infrastructure.security.provider import get_current_actor
from app.infrastructure.settings.provider import (
    get_app_system_session,
    get_app_user_session
)

from app.feature.session.uow.session_uow_port import SessionUoWPort
from app.feature.stripe.uow.stripe_uow_port import StripeUoWPort
from app.infrastructure.persistence.sqlalchemy.uow.stripe.stripe_uow import (
    SqlAlchemyStripeUoW
)


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


async def get_me_system_uow(
    session: AsyncSession = Depends(get_app_system_session),
    actor: Actor = Depends(get_current_actor)
) -> MeSystemUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {"user_id": str(actor.id)},
    )
    return SqlAlchemyMeSystemUoW(session)


async def get_session_public_uow(
    session: AsyncSession = Depends(get_app_user_session),
) -> SessionPulbicUoWPort:
    return SqlAlchemySessionPublicUoW(session)


async def get_session_uow(
    actor: Actor = Depends(get_current_actor),
    session: AsyncSession = Depends(get_app_system_session)
) -> SessionUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {"user_id": str(actor.id)},
    )

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


async def get_admin_system_user_uow(
        session: AsyncSession = Depends(get_app_system_session),
        actor: Actor = Depends(get_current_actor)
) -> AdminUserSystemUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {"user_id": str(actor.id)},
    )
    return SqlAlchemyAdminUserSystemUoW(session)


async def get_credit_uow(
        session: AsyncSession = Depends(get_app_user_session),
        actor: Actor = Depends(get_current_actor)
) -> CreditUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {
            "user_id": str(actor.id)
        }
    )
    return SqlAlchemyCreditUoW(session)


async def get_payment_uow(
        session: AsyncSession = Depends(get_app_user_session),
        actor: Actor = Depends(get_current_actor)
) -> PaymentUoWPort:
    await session.execute(
        text(
            "SELECT set_config('app.current_user_id', :user_id, true)"
        ),
        {
            "user_id": str(actor.id)
        }
    )
    return SqlAlchemyPaymenUoW(session)


async def get_stripe_uow(
    session: AsyncSession = Depends(get_app_system_session)
) -> StripeUoWPort:
    return SqlAlchemyStripeUoW(session)
