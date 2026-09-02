import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.interaction import Interaction


class InteractionRepository:
    @staticmethod
    def get_by_id(db: Session, interaction_id: uuid.UUID) -> Optional[Interaction]:
        return db.query(Interaction).filter(Interaction.id == interaction_id).first()

    @staticmethod
    def get_by_case_id(db: Session, case_id: uuid.UUID) -> List[Interaction]:
        return (
            db.query(Interaction)
            .filter(Interaction.case_id == case_id)
            .order_by(Interaction.occurred_at.desc())
            .all()
        )

    @staticmethod
    def create(db: Session, interaction: Interaction) -> Interaction:
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return interaction
