from datetime import datetime
import uuid

from sqlalchemy import INTEGER, UUID, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.persistence.sqlalchemy.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": "app"}

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    role_id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )
