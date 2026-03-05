from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


def create_session_factory(
    engine: AsyncEngine
) -> async_sessionmaker[AsyncSession]:
    """Create an async SQLAlchemy session factory.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.

    Returns:
        async_sessionmaker[AsyncSession]: Session factory.
    """
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
