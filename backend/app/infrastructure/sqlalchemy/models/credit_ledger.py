from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.sqlalchemy.base import Base
from sqlalchemy.dialects.postgresql import ENUM
from app.domain.credit.credit_cause import CreditCause


class CreditLedger(Base):
    __tablename__ = "credit_ledger"
    __table_args__ = {"schema": "app"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    payment_intent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)

    balance_after_cents: Mapped[int] = mapped_column(Integer, nullable=False)

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
        nullable=False
    )
