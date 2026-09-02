import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.distress_score import DistressScore


class DistressScoreRepository:
    @staticmethod
    def get_by_id(db: Session, score_id: uuid.UUID) -> Optional[DistressScore]:
        return db.query(DistressScore).filter(DistressScore.id == score_id).first()

    @staticmethod
    def get_by_assessment_id(
        db: Session, assessment_id: uuid.UUID
    ) -> Optional[DistressScore]:
        return (
            db.query(DistressScore)
            .filter(DistressScore.assessment_id == assessment_id)
            .first()
        )

    @staticmethod
    def get_history_by_case_id(
        db: Session, case_id: uuid.UUID
    ) -> List[DistressScore]:
        return (
            db.query(DistressScore)
            .filter(DistressScore.case_id == case_id)
            .order_by(DistressScore.computed_at.asc())
            .all()
        )

    @staticmethod
    def get_first_by_case_id(
        db: Session, case_id: uuid.UUID
    ) -> Optional[DistressScore]:
        return (
            db.query(DistressScore)
            .filter(DistressScore.case_id == case_id)
            .order_by(DistressScore.computed_at.asc())
            .first()
        )

    @staticmethod
    def get_latest_by_case_id(
        db: Session, case_id: uuid.UUID
    ) -> Optional[DistressScore]:
        return (
            db.query(DistressScore)
            .filter(DistressScore.case_id == case_id)
            .order_by(DistressScore.computed_at.desc())
            .first()
        )

    @staticmethod
    def create(db: Session, score: DistressScore) -> DistressScore:
        db.add(score)
        db.commit()
        db.refresh(score)
        return score
