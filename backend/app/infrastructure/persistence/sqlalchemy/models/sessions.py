from datetime import datetime
import uuid

from sqlalchemy import UUID, VARCHAR, DateTime, Enum, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from app.domain.session.session_status import SessionStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .payment import Payment
    from .session_attendance import SessionAttendance
    from .session_participation import SessionParticipation
    from .users import User


class Session(Base):
    """Represents a scheduled session led by a coach.

    A session defines a time-bounded event that users may participate
    in. Each session is owned by a coach and may accept multiple
    participants. Sessions have a lifecycle represented by their
    status and may be cancelled without being deleted.

    Sessions act as the aggregate root for participation, attendance,
    and payment records. Related entities reference the session to
    enforce integrity and support auditing.

    Attributes:
        id (uuid.UUID): Unique identifier of the session.
        coach_id (uuid.UUID): Identifier of the user acting as the coach.
        title (str): Human-readable title of the session.
        starts_at (datetime): Timestamp when the session begins.
        ends_at (datetime): Timestamp when the session ends.
        status (SessionStatus): Current lifecycle status of the session.
        cancelled_at (datetime | None): Timestamp when the session was
            cancelled, or None if the session is active.
        created_at (datetime): Timestamp when the session was created.
        updated_at (datetime): Timestamp when the session was last
            updated.

    Relationships:
        session_payments (list[Payment]): Payments associated with the
            session.
        session_attendance (list[SessionAttendance]): Attendance records
            recorded for the session.
        session_participations (list[SessionParticipation]): User
            participations registered for the session.
        coach (User): User responsible for leading the session.
    """

    __tablename__ = "sessions"
    __table_args__ = {"schema": "app"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    coach_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.users.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        VARCHAR(128),
        nullable=False
    )

    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    status: Mapped[SessionStatus] = mapped_column(
        Enum(
            SessionStatus,
            name="session_status",
            schema="app",
            native_enum=True,
            create_constraint=False,  # DB already owns it
        ),
        nullable=False,
    )

    cancelled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )

    session_payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="session"
    )

    session_attendance: Mapped[list["SessionAttendance"]] = relationship(
        "SessionAttendance",
        back_populates="session",
        lazy="selectin"
    )

    session_participations: Mapped[list["SessionParticipation"]] = (
        relationship(
            "SessionParticipation",
            back_populates="session",
            lazy="selectin"
        )
    )

    coach: Mapped["User"] = relationship(
        "User",
        foreign_keys=[coach_id],
        lazy="joined"
    )
