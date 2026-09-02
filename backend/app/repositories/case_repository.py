import uuid
from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.case import Case


class CaseRepository:
    @staticmethod
    def get_by_id(db: Session, case_id: uuid.UUID) -> Optional[Case]:
        return db.query(Case).filter(Case.id == case_id).first()

    @staticmethod
    def get_by_victim_id(db: Session, victim_id: uuid.UUID) -> List[Case]:
        return db.query(Case).filter(Case.victim_id == victim_id).all()

    @staticmethod
    def create(db: Session, case: Case) -> Case:
        db.add(case)
        db.commit()
        db.refresh(case)
        return case

    @staticmethod
    def update(db: Session, case: Case) -> Case:
        db.commit()
        db.refresh(case)
        return case
