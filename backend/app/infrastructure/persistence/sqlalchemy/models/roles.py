from datetime import datetime
from sqlalchemy import INTEGER, VARCHAR, DateTime, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.persistence.sqlalchemy.base import Base


class Role(Base):
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
