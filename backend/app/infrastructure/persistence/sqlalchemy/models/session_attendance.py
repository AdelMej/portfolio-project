from datetime import datetime
import uuid
from sqlalchemy import UUID, Boolean, DateTime, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.persistence.sqlalchemy.base import Base


class SessionAttendance(Base):
    __tablename__ = "session_attendance"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "user_id",
            name="uq_session_attendance_user_session"
        ),
        {"schema": "app"}
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    attended: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )

    recorded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )
