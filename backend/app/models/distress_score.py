import uuid
from typing import TYPE_CHECKING
from sqlalchemy import Float, String, DateTime, ForeignKey, func, Uuid, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.case import Case
    from app.models.assessment import Assessment


class DistressScore(Base):
    __tablename__ = "distress_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("cases.id", ondelete="CASCADE"), index=True, nullable=False
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("assessments.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    current_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # 0.0 to 100.0 DDS
    baseline_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # 0.0 to 100.0 (first assessment DDS)
    trend_slope: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )  # Rate of change / slope across recent assessments
    risk_band: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # low, moderate, high, critical
    computed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    case: Mapped["Case"] = relationship("Case", back_populates="distress_scores")
    assessment: Mapped["Assessment"] = relationship(
        "Assessment", back_populates="distress_score"
    )

    __table_args__ = (
        Index("ix_distress_scores_case_id_computed_at", "case_id", "computed_at"),
    )
