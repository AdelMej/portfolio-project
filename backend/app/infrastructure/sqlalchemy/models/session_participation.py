from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.sqlalchemy.base import Base


class SessionParticipation(Base):
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
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
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
