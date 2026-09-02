import uuid
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func, Uuid, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.case import Case
    from app.models.assessment import Assessment


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("cases.id", ondelete="CASCADE"), index=True, nullable=False
    )
    channel: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # chatbot, ivrs, sms, app, web
    raw_ref_pointer: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Pointer to isolated encrypted store (Section 10 & 19)
    response_latency_sec: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    was_skipped: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    occurred_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship("Case", back_populates="interactions")
    assessment: Mapped["Assessment | None"] = relationship(
        "Assessment", back_populates="interaction", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_interactions_case_id_occurred_at", "case_id", "occurred_at"),
    )
