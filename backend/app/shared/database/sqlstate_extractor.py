from sqlalchemy.exc import DBAPIError
from typing import Optional


def get_sqlstate(exc: DBAPIError) -> Optional[str]:
    orig = exc.orig

    if orig is None:
        return None

    # asyncpg
    if hasattr(orig, "sqlstate"):
        return getattr(orig, "sqlstate")

    # psycopg
    if hasattr(orig, "pgcode"):
        return getattr(orig, "pgcode")

    return None
