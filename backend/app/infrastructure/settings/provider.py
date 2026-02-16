from typing import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.infrastructure.settings.app_settings import AppSettings


def get_settings(request: Request) -> AppSettings:
    return request.app.state.settings


def get_refresh_token_ttl(request: Request) -> int:
    return request.app.state.settings.jwt_refresh_ttl_seconds


def get_access_token_ttl(request: Request) -> int:
    return request.app.state.settings.jwt_access_ttl_seconds


def get_jwt_algorithm(request: Request) -> str:
    return request.app.state.settings.jwt_algorithm


def get_jwt_secret(request: Request) -> str:
    return request.app.state.settings.jwt_secret


def get_jwt_issuer(request: Request) -> str:
    return request.app.state.settings.jwt_issuer


def get_token_hmac_secret(request: Request) -> str:
    return request.app.state.settings.refresh_token_hmac_secret


def get_web_hook_secret(request: Request) -> str:
    return request.app.state.settings.stripe_webhook_secret


def get_app_user_engine(request: Request) -> str:
    return request.app.state.settings.app_system_dsn()


async def get_app_user_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.app_user_session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_app_system_session(
    request: Request
) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.app_system_session_factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
