from datetime import datetime
import uuid

from sqlalchemy import INTEGER, UUID, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .roles import Role


class UserRole(Base):
    """Represents the assignment of a role to a user.

    A user role links a user to a role and records when the role was
    granted. Each role may be assigned to a given user at most once,
    enforced by a composite primary key.

    User-role assignments are append-only and are not updated or
    deleted. Revocation or expiration, if needed, should be modeled via
    additional state rather than mutation.

    Attributes:
        user_id (uuid.UUID): Identifier of the user receiving the role.
        role_id (int): Identifier of the assigned role.
        assigned_at (datetime): Timestamp when the role was assigned.

    Relationships:
        user (User): User to whom the role is assigned.
        role (Role): Role assigned to the user.
    """

    __tablename__ = "user_roles"
    __table_args__ = {"schema": "app"}

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.users.id"),
        primary_key=True
    )

    role_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("app.roles.id"),
        primary_key=True
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_roles",
        lazy="joined"
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="user_roles",
        lazy="joined"
    )
