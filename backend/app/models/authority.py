import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.case import Case


class Authority(Base):
    __tablename__ = "authorities"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    jurisdiction_level: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # district, state, national
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="authority"
    )
    assigned_cases: Mapped[List["Case"]] = relationship(
        "Case", back_populates="assigned_authority"
    )
