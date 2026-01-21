from datetime import datetime
import uuid

from sqlalchemy import UUID, BigInteger, DateTime, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.sqlalchemy.base import Base


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        UniqueConstraint(
            "token_hash",
            name="uq_refresh_tokens_token_hash"
        ),
        {"schema": "app"},
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    token_hash: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    replaced_by_token: Mapped[int] = mapped_column(
        BigInteger,
        nullable=True
    )
