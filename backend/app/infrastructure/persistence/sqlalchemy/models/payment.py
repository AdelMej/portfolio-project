from datetime import datetime
import uuid
from sqlalchemy import CHAR, UUID, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import UniqueConstraint
from app.infrastructure.persistence.sqlalchemy.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from sessions import Session


class Payment(Base):
    """Represents a payment recorded with an external payment provider.

    This table stores immutable payment records associated with a user
    and a session. Each payment corresponds to a provider-specific
    payment intent and is uniquely identified per provider.

    Payments are treated as append-only records and are not updated
    after creation. They serve as the source of truth for monetary
    inflows and may be referenced by downstream processes such as
    credit ledger entries or audits.

    Attributes:
        id (uuid.UUID): Unique identifier of the payment.
        session_id (uuid.UUID): Identifier of the session associated
            with this payment.
        user_id (uuid.UUID): Identifier of the user who made the payment.
        provider (str): Name of the external payment provider.
        provider_intent_id (str): Provider-specific payment intent
            identifier.
        amount_cents (int): Payment amount in cents.
        currency (str): ISO 4217 currency code (e.g. "EUR", "USD").
        created_at (datetime): Timestamp when the payment record was
            created.

    Relationships:
        session (Session): Session associated with this payment.
        user (User): User who made this payment.
    """

    __tablename__ = "payment"
    __table_args__ = (
        UniqueConstraint(
                "provider",
                "provider_intent_id",
                name="uq_payment_provider_id",
            ),
        {"schema": "app"},
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

    provider: Mapped[str] = mapped_column(nullable=False)

    provider_intent_id: Mapped[str] = mapped_column(nullable=False)

    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="session_payments",
        lazy="joined"
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_payments",
        lazy="joined"
    )
