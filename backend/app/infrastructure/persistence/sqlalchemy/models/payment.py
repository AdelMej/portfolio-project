from datetime import datetime
import uuid
from sqlalchemy import CHAR, UUID, DateTime, Integer, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import UniqueConstraint
from app.infrastructure.persistence.sqlalchemy.base import Base


class Payment(Base):
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
        nullable=False
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
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
