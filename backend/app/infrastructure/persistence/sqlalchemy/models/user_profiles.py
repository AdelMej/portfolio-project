from datetime import datetime
import uuid

from sqlalchemy import UUID, VARCHAR, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.persistence.sqlalchemy.base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {"schema": "app"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False
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
