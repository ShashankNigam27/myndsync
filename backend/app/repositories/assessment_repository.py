import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.assessment import Assessment


class AssessmentRepository:
    @staticmethod
    def get_by_id(db: Session, assessment_id: uuid.UUID) -> Optional[Assessment]:
        return db.query(Assessment).filter(Assessment.id == assessment_id).first()

    @staticmethod
    def get_by_interaction_id(
        db: Session, interaction_id: uuid.UUID
    ) -> Optional[Assessment]:
        return (
            db.query(Assessment)
            .filter(Assessment.interaction_id == interaction_id)
            .first()
        )

    @staticmethod
    def create(db: Session, assessment: Assessment) -> Assessment:
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        return assessment
