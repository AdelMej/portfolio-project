from datetime import datetime
import uuid

from sqlalchemy import (
    UUID,
    BigInteger,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User


class RefreshToken(Base):
    """Represents a rotating refresh token used for authentication.

    Refresh tokens are long-lived credentials issued to a user and are
    rotated on use. Each token is immutable and may be revoked or
    replaced by a newer token, forming a lineage that enables replay
    detection and auditability.

    Tokens are stored as hashes and are never updated or deleted.
    Revocation and rotation are recorded via timestamps and
    self-referential relationships.

    Attributes:
        id (int): Unique identifier of the refresh token.
        user_id (uuid.UUID): Identifier of the user to whom the token
            was issued.
        token_hash (str): Hash of the refresh token value.
        created_at (datetime): Timestamp when the token was created.
        expires_at (datetime): Timestamp after which the token is no
            longer valid.
        revoked_at (datetime | None): Timestamp when the token was
            revoked, or None if it is still valid.
        replaced_by_token_id (uuid.UUID | None): Identifier of the token
            that replaced this one during rotation.

    Relationships:
        replaced_by_token (RefreshToken | None): Token that replaced
            this token.
        replaced_tokens (list[RefreshToken]): Tokens that were replaced
            by this token.
        user (User): User who owns this refresh token.
    """

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
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.users.id", ondelete="CASCADE"),
        nullable=False
    )

    token_hash: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    replaced_by_token_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("app.refresh_tokens.id"),
        nullable=True
    )

    replaced_by_token: Mapped["RefreshToken | None"] = relationship(
        "RefreshToken",
        remote_side="RefreshToken.id",
        back_populates="replaced_tokens"
    )

    replaced_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="replaced_by_token"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens",
        lazy="joined"
    )
