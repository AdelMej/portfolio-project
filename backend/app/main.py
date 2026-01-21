from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.infrastructure.settings.app_settings import AppSettings
from app.infrastructure.persistence.sqlalchemy.engines import (
    create_app_engine,
    create_system_engine,
)
from app.infrastructure.persistence.sqlalchemy.sessions import (
    create_session_factory,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Initializes database engines and session factories and validates
    database connectivity at startup.
    """
    settings = AppSettings()  # pyright: ignore[reportCallIssue]

    app_engine = create_app_engine(settings)
    system_engine = create_system_engine(settings)

    async with app_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    async with system_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    app.state.settings = settings
    app.state.app_engine = app_engine
    app.state.system_engine = system_engine
    app.state.app_session_factory = create_session_factory(app_engine)
    app.state.system_session_factory = create_session_factory(system_engine)

    yield

    await app_engine.dispose()
    await system_engine.dispose()


app = FastAPI(lifespan=lifespan)
