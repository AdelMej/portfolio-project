from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import UUID, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from sqlalchemy.dialects.postgresql import ENUM
from app.domain.credit.credit_cause import CreditCause


if TYPE_CHECKING:
    from .users import User
    from .payment_intents import PaymentIntent


class CreditLedger(Base):
    """Append-only ledger entry representing a credit mutation for a user.

    This table records all credit balance changes as immutable events.
    Each entry represents a single credit mutation (positive or
    negative) and stores the resulting balance after the mutation for
    auditability and historical reconstruction.

    The ledger is append-only by design:
    entries are never updated or deleted once created.

    Attributes:
        id (uuid.UUID): Unique identifier of the ledger entry.
        user_id (uuid.UUID): Identifier of the user whose balance is
            affected.
        payment_intent_id (uuid.UUID | None): Optional payment intent
            associated with this credit mutation.
        amount_cents (int): Signed amount applied to the user's balance,
            in cents. Positive values represent credits, negative values
            represent debits.
        balance_after_cents (int): User balance in cents after applying
            this entry.
        cause (CreditCause): Business cause of the credit mutation.
        created_at (datetime): Timestamp when the ledger entry was
            created.

    Relationships:
        user (User): User associated with this ledger entry.
        payment_intent (PaymentIntent | None): Payment intent related to
            this credit mutation, if applicable.
    """
    __tablename__ = "credit_ledger"
    __table_args__ = {"schema": "app"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.users.id"),
        nullable=False
    )

    payment_intent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.payment_intents.id"),
        nullable=True
    )

    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    balance_after_cents: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    cause: Mapped[CreditCause] = mapped_column(
        ENUM(
            CreditCause,
            name="credit_ledger_cause",
            schema="app",
            create_type=False
        ),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="credit_ledger_entries",
        lazy="joined",
    )

    payment_intent: Mapped["PaymentIntent | None"] = relationship(
        "PaymentIntent",
        back_populates="ledger_entry",
        lazy="joined",
    )
