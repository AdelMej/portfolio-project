from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .session_attendance import SessionAttendance
    from .users import User
    from .sessions import Session


class SessionParticipation(Base):
    """Represents a user's participation in a session.

    A session participation links a user to a session and represents
    their registration state. Each user may participate in a given
    session at most once, enforced by a composite uniqueness constraint.

    Participation records are created when a user registers for a
    session and may later be cancelled. Attendance records may be
    associated with a participation to record actual presence.

    Attributes:
        id (uuid.UUID): Unique identifier of the participation record.
        session_id (uuid.UUID): Identifier of the associated session.
        user_id (uuid.UUID): Identifier of the participating user.
        registered_at (datetime): Timestamp when the user registered
            for the session.
        cancelled_at (datetime | None): Timestamp when the participation
            was cancelled, or None if it is still active.

    Relationships:
        attendance_entries (list[SessionAttendance]): Attendance records
            associated with this participation.
        session (Session): Session in which the user participates.
        user (User): User who participates in the session.
    """

    __tablename__ = "session_participation"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "user_id",
            name="uq_session_participation_user_session"
        ),
        {"schema": "app"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.sessions.id"),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.users.id"),
        nullable=False
    )

    paid_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )

    cancelled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    attendance_entries: Mapped[list["SessionAttendance"]] = relationship(
        "SessionAttendance",
        lazy="selectin",
    )

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="session_participations",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="participations",
    )
