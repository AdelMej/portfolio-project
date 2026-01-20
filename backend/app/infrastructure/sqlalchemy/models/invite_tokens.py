from datetime import datetime
import uuid

from sqlalchemy import DATETIME, UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.sqlalchemy.base import Base


class InviteTokens(Base):
    __tablename__ = "invite_tokens"
    __table_args__ = {"schema": "app"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    token_hash: Mapped[str] = mapped_column(nullable=False, unique=True)

    expires_at: Mapped[datetime] = mapped_column(
        DATETIME(timezone=True),
        nullable=False
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        init=False
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
