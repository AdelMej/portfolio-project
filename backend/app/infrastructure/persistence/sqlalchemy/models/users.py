from typing import TYPE_CHECKING
from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime, UniqueConstraint, text
from app.infrastructure.persistence.sqlalchemy.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT

if TYPE_CHECKING:
    from .credit_ledger import CreditLedger

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            "email",
            name="uq_users_email"
        ),
        {"schema": "app"}
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)

    email: Mapped[str] = mapped_column(CITEXT, nullable=False)

    password_hash: Mapped[str] = mapped_column(nullable=False)

    disabled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    disabled_reason: Mapped[str | None] = mapped_column(nullable=True)
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

    credit_ledger_entries: Mapped[list["CreditLedger"]] = relationship(
        "CreditLedger",
        back_populates="user",
        lazy="selectin",
        cascade="none",
        passive_deletes=True,
    )
