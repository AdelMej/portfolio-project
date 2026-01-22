from datetime import datetime
import uuid

from sqlalchemy import UUID, VARCHAR, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User


class UserProfile(Base):
    """Represents a user's profile information.

    A user profile stores personal, non-authentication-related
    information associated with a user. The profile shares its primary
    key with the user entity, enforcing a strict one-to-one relationship
    at the database level.

    A profile cannot exist without a corresponding user and acts as an
    extension of the user entity rather than an independent aggregate.

    Attributes:
        user_id (uuid.UUID): Identifier of the user to whom this profile
            belongs. Serves as both the primary key and a foreign key.
        first_name (str): User's first name.
        last_name (str): User's last name.
        created_at (datetime): Timestamp when the profile was created.
        updated_at (datetime): Timestamp when the profile was last
            updated.

    Relationships:
        user (User): User associated with this profile.
    """

    __tablename__ = "user_profiles"
    __table_args__ = {"schema": "app"}

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("app.users.id"),
        primary_key=True
    )

    first_name: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False
    )

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
        back_populates="user_profile",
        lazy="joined"
    )
