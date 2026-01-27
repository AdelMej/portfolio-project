from datetime import datetime
import uuid
from sqlalchemy import (
    UUID,
    Boolean,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    UniqueConstraint,
    text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .sessions import Session


class SessionAttendance(Base):
    """Represents an attendance record for a session participant.

    Attendance records capture whether a specific user attended a given
    session. Each attendance entry is associated with an existing
    session participation, ensuring that attendance can only be
    recorded for users who are registered as participants.

    The combination of session and user is unique, preventing duplicate
    attendance records. Attendance is append-only and recorded with
    explicit metadata for auditability.

    Attributes:
        id (uuid.UUID): Unique identifier of the attendance record.
        session_id (uuid.UUID): Identifier of the session attended.
        user_id (uuid.UUID): Identifier of the user whose attendance was
            recorded.
        attended (bool): Indicates whether the user attended the session.
        recorded_at (datetime): Timestamp when the attendance was
            recorded.
        recorded_by (uuid.UUID): Identifier of the actor who recorded
            the attendance.
    """

    __tablename__ = "session_attendance"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "user_id",
            name="uq_session_attendance_user_session"
        ),
        ForeignKeyConstraint(
            ["session_id", "user_id"],
            [
                "app.session_participation.session_id",
                "app.session_participation.user_id",
            ],
            ondelete="RESTRICT",
            name="fk_attendance_participation"
        ),
        {"schema": "app"}
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

    attended: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    recorded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="attendance",
        lazy="selectin"
    )

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="session_attendance"
    )
