from datetime import datetime
from sqlalchemy import INTEGER, VARCHAR, DateTime, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.persistence.sqlalchemy.base import Base
from sqlalchemy.ext.associationproxy import association_proxy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user_roles import UserRole


class Role(Base):
    """Represents a role used for authorization.

    Roles define named permission groupings that can be assigned to users
    or other actors within the system. Each role is uniquely identified
    by its name and is immutable after creation.

    Roles are append-only and are intended to be stable identifiers used
    throughout the authorization layer.

    Attributes:
        id (int): Unique identifier of the role.
        role_name (str): Unique name of the role.
        created_at (datetime): Timestamp when the role was created.

    Relationships:
        user_roles (list[UserRole]): User-role assignment records
            associated with this role.

    Proxies:
        users (list[User]): Users to whom this role is assigned, exposed
            via an association proxy.
    """

    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint(
            "role_name",
            name="uq_roles_role_name"
        ),
        {"schema": "app"},
    )

    id: Mapped[int] = mapped_column(
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    role_name: Mapped[str] = mapped_column(
        VARCHAR(64),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
        init=False
    )

    user_roles: Mapped[list["UserRole"]] = relationship(
        "UserRole",
        back_populates="role",
        lazy="selectin"
    )

    users = association_proxy(
        "user_roles",
        "user"
    )
