from typing import TYPE_CHECKING
from datetime import datetime
import uuid
from sqlalchemy import UUID, DateTime, UniqueConstraint, text
from app.infrastructure.persistence.sqlalchemy.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.ext.associationproxy import association_proxy


if TYPE_CHECKING:
    from .credit_ledger import CreditLedger
    from .payment import Payment
    from .payment_intents import PaymentIntent
    from .refresh_tokens import RefreshToken
    from .session_attendance import SessionAttendance
    from .session_participation import SessionParticipation
    from .user_profiles import UserProfile
    from .user_roles import UserRole


class User(Base):
    """Represents an authenticated user of the system.

    A user is the core identity within the system and owns credentials,
    roles, and security artifacts. Users may participate in sessions,
    make payments, and hold account-level state such as credit balances.

    Users are never deleted. Disabling a user records a timestamp and
    reason to preserve auditability and historical references.

    Attributes:
        id (uuid.UUID): Unique identifier of the user.
        email (str): Unique email address used for authentication.
        password_hash (str): Hashed user password.
        disabled_at (datetime | None): Timestamp when the user was
            disabled, or None if the user is active.
        disabled_reason (str | None): Reason for disabling the user.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.

    Relationships:
        credit_ledger_entries (list[CreditLedger]): Credit ledger entries
            associated with the user.
        user_payments (list[Payment]): Payments made by the user.
        user_payment_intents (list[PaymentIntent]): Payment intents
            initiated by the user.
        refresh_tokens (list[RefreshToken]): Refresh tokens issued to the
            user.
        attendance (list[SessionAttendance]): Attendance records for
            sessions attended by the user.
        participations (list[SessionParticipation]): Session
            participations registered by the user.
        user_profiles (UserProfile): Profile information associated with
            the user.
        user_roles (list[UserRole]): Role assignments for the user.

    Proxies:
        roles (list[Role]): Roles assigned to the user, exposed via an
            association proxy.
    """

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
        server_default=text("now()")
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    credit_ledger_entries: Mapped[list["CreditLedger"]] = relationship(
        "CreditLedger",
        back_populates="user",
        lazy="selectin",
    )

    user_payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="user",
    )

    user_payment_intents: Mapped[list["PaymentIntent"]] = relationship(
        "PaymentIntent",
        back_populates="user"
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        lazy="selectin"
    )

    attendance: Mapped[list["SessionAttendance"]] = relationship(
        "SessionAttendance",
        back_populates="user",
        lazy="selectin",
        overlaps="attendance_entries",
    )

    participations: Mapped[list["SessionParticipation"]] = relationship(
        "SessionParticipation",
        back_populates="user",
        lazy="selectin"
    )

    user_profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="user",
        lazy="joined",
        uselist=False
    )

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="user",
        lazy="selectin"
    )

    roles = association_proxy(
        "user_roles",
        "role"
    )
