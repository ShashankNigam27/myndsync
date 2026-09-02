import uuid
from typing import TYPE_CHECKING
from sqlalchemy import Float, String, DateTime, ForeignKey, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.interaction import Interaction
    from app.models.distress_score import DistressScore


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    interaction_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("interactions.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    sentiment_score: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # -1.0 (most negative/distressed) to +1.0 (positive)
    emotion_label: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # optional: fear, sadness, anger, hopelessness, neutral
    voice_stress_score: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # optional: 0.0 to 1.0 (when voice used)
    confidence: Mapped[float] = mapped_column(
        Float, default=1.0, nullable=False
    )  # 0.0 to 1.0
    processed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    interaction: Mapped["Interaction"] = relationship(
        "Interaction", back_populates="assessment"
    )
    distress_score: Mapped["DistressScore | None"] = relationship(
        "DistressScore", back_populates="assessment", uselist=False, cascade="all, delete-orphan"
    )
