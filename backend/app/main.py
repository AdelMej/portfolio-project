from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

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
from app.feature.auth.auth_router import router as auth_router
from app.feature.admin.users.admin_users_router import (
    router as admin_users_router
)
from app.shared.handlers import register_exception_handlers
import logging

from app.feature.session.session_router import router as session_router
from app.feature.credit.credit_router import router as credit_router
from app.feature.payment.payment_router import router as payment_router

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(name)s - %(message)s",
)



@asynccontextmanager
async def lifespan(api: FastAPI):
    """Application lifespan handler.

    Initializes database engines and session factories and validates
    database connectivity at startup.
    """
    import app.infrastructure.persistence.sqlalchemy.models  # noqa: F401

    settings = AppSettings()  # pyright: ignore[reportCallIssue]

    app_user_engine = create_app_engine(settings.app_user_dsn())
    app_system_engine = create_system_engine(settings.app_system_dsn())

    try:
        async with app_user_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise RuntimeError("app_user DB connection failed") from exc

    try:
        async with app_system_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as exc:
        raise RuntimeError("app_system DB connection failed") from exc

    api.state.settings = settings
    api.state.app_user_engine = app_user_engine
    api.state.app_system_engine = app_system_engine
    api.state.app_user_session_factory = create_session_factory(
        app_user_engine
    )
    api.state.app_system_session_factory = create_session_factory(
        app_system_engine
    )

    yield

    await app_user_engine.dispose()
    await app_system_engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(session_router, prefix="/sessions", tags=["sessions"])
app.include_router(admin_users_router)
app.include_router(credit_router)
app.include_router(payment_router)


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    """
    Liveness probe endpoint.

    This endpoint is used to verify that the application process is running
    and able to handle incoming HTTP requests. It performs no external
    dependency checks and always returns a static response.

    Intended usage:
    - Container liveness checks (Docker, Kubernetes)
    - Basic uptime monitoring

    This endpoint MUST remain fast, side-effect free, and always available.
    """
    return {"status": "ok"}
