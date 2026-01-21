from datetime import datetime
import uuid
from sqlalchemy import CHAR, INTEGER, UUID, DateTime, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.persistence.sqlalchemy.base import Base


class PaymentIntents(Base):
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
        nullable=False
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
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
