import uuid
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.victim import Victim
    from app.models.authority import Authority
    from app.models.interaction import Interaction
    from app.models.distress_score import DistressScore


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    victim_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("victims.id", ondelete="CASCADE"), index=True, nullable=False
    )
    crime_category: Mapped[str] = mapped_column(String(100), nullable=False)
    legal_stage: Mapped[str | None] = mapped_column(String(100), nullable=True)
    assigned_authority_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("authorities.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False
    )  # active, closed, reopened
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    closed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    victim: Mapped["Victim"] = relationship("Victim", back_populates="cases")
    assigned_authority: Mapped["Authority | None"] = relationship(
        "Authority", back_populates="assigned_cases"
    )
    interactions: Mapped[List["Interaction"]] = relationship(
        "Interaction", back_populates="case", cascade="all, delete-orphan"
    )
    distress_scores: Mapped[List["DistressScore"]] = relationship(
        "DistressScore", back_populates="case", cascade="all, delete-orphan"
    )
