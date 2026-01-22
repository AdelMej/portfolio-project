from datetime import datetime
import uuid
from sqlalchemy import CHAR, INTEGER, UUID, DateTime, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .sessions import Session


class PaymentIntent(Base):
    """Represents a payment intent created with an external provider.

    A payment intent models the lifecycle of a payment attempt with an
    external payment provider. It records the expected amount, currency,
    current status, and whether credit has already been applied as a
    result of this intent.

    Payment intents are immutable with respect to their monetary
    attributes. State transitions are tracked through status changes
    and related records such as payments or credit ledger entries.

    Attributes:
        id (uuid.UUID): Unique identifier of the payment intent.
        user_id (uuid.UUID): Identifier of the user initiating the
            payment intent.
        session_id (uuid.UUID): Identifier of the session associated
            with this payment intent.
        provider (str): Name of the external payment provider.
        provider_intent_id (str): Provider-specific payment intent
            identifier.
        status (str): Current status of the payment intent as reported
            by the provider.
        credit_applied (int): Amount of credit, in cents, already
            applied as a result of this payment intent.
        amount_cents (int): Intended payment amount in cents.
        currency (str): ISO 4217 currency code (e.g. "EUR", "USD").
        created_at (datetime): Timestamp when the payment intent was
            created.
        updated_at (datetime): Timestamp when the payment intent was
            last updated.

    Relationships:
        user (User): User who initiated this payment intent.
        session (Session): Session associated with this payment intent.
    """

    __tablename__ = "payment_intents"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_intent_id",
            name="uq_payment_intents_provider_intent",
        ),
        {"schema": "app"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.users.id"),
        nullable=False
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.sessions.id"),
        nullable=False
    )

    provider: Mapped[str] = mapped_column(nullable=False)

    provider_intent_id: Mapped[str] = mapped_column(nullable=False)

    status: Mapped[str] = mapped_column(nullable=False)

    credit_applied: Mapped[int] = mapped_column(INTEGER, nullable=False)

    amount_cents: Mapped[int] = mapped_column(INTEGER, nullable=False)

    currency: Mapped[str] = mapped_column(CHAR(3), nullable=False)

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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_payment_intents",
        lazy="joined"
    )

    session: Mapped["Session"] = relationship(
        "Session",
        back_populates="session_payment_intents",
        lazy="joined"
    )
