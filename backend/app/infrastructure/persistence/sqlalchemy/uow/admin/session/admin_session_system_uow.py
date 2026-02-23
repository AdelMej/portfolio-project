from sqlalchemy.ext.asyncio.session import AsyncSession
from app.feature.admin.session.uow.admin_session_system_uow_port import (
    AdminSessionSystemUoWPort
)
from app.infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyAuthReadRepo,
    SqlAlchemyAdminSessionReadRepo,
    SqlAlchemyAdminSessionUpdateRepo,
    SqlAlchemyAdminSessionAttendanceReadRepo
)


class SqlAlchemyAdminSessionSystemUoW(AdminSessionSystemUoWPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.auth_read_repo = SqlAlchemyAuthReadRepo(session)
        self.session_read_repo = SqlAlchemyAdminSessionReadRepo(session)
        self.session_update_repo = SqlAlchemyAdminSessionUpdateRepo(session)
        self.session_attendance_read_repo = (
            SqlAlchemyAdminSessionAttendanceReadRepo(session)
        )
