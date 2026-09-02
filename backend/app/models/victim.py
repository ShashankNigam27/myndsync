import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.case import Case


class Victim(Base):
    __tablename__ = "victims"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    case_ref_id: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    preferred_language: Mapped[str] = mapped_column(
        String(10), default="hi", nullable=False
    )
    preferred_channel: Mapped[str] = mapped_column(
        String(20), default="sms", nullable=False
    )  # chatbot, ivrs, sms, app, web
    consent_status: Mapped[str] = mapped_column(
        String(20), default="pending", nullable=False
    )  # active, revoked, pending
    enrolled_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
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
    cases: Mapped[List["Case"]] = relationship(
        "Case", back_populates="victim", cascade="all, delete-orphan"
    )
