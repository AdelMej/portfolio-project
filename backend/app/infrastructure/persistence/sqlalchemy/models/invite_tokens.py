from datetime import datetime
import uuid

from sqlalchemy import DATETIME, UUID, DateTime, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.persistence.sqlalchemy.base import Base


class InviteTokens(Base):
    """Represents a single-use invitation token.

    Invitation tokens are used to grant controlled access to the system,
    typically for onboarding new users. Tokens are stored as hashes and
    have a fixed expiration time.

    Tokens are immutable and never deleted. Usage is recorded by setting
    the `used_at` timestamp, allowing replay prevention, auditing, and
    abuse detection.

    Attributes:
        id (uuid.UUID): Unique identifier of the invitation token.
        token_hash (str): Hash of the invitation token value.
        expires_at (datetime): Timestamp after which the token is no
            longer valid.
        used_at (datetime | None): Timestamp when the token was used, or
            None if it has not been consumed.
        created_at (datetime): Timestamp when the token was created.
        created_by (uuid.UUID): Identifier of the actor who created the
            invitation token.
    """

    __tablename__ = "invite_tokens"
    __table_args__ = (
        UniqueConstraint(
            "token_hash",
            name="uq_invite_tokens_token_hash"
        ),
        {"schema": "app"},
    )

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
        server_default=text("now()")
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
