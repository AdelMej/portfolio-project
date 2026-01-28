from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def create_app_engine(dsn: str) -> AsyncEngine:
    """Create the application database engine.

    Uses the application role which is subject to RLS and business rules.

    Args:
        settings (AppSettings): Application settings.

    Returns:
        AsyncEngine: SQLAlchemy async engine.
    """
    return create_async_engine(
        dsn,
        echo=False,
        pool_pre_ping=True,
    )


def create_system_engine(dsn: str) -> AsyncEngine:
    """Create the system database engine.

    Uses the system role for internal operations that require elevated
    permissions but still respect RLS where applicable.

    Args:
        settings (AppSettings): Application settings.

    Returns:
        AsyncEngine: SQLAlchemy async engine.
    """
    return create_async_engine(
        dsn,
        echo=False,
        pool_pre_ping=True,
    )
