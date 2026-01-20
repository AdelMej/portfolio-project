import uuid
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.schema import UniqueConstraint
from app.infrastructure.sqlalchemy.base import Base


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


