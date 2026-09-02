import uuid
from typing import Optional
from sqlalchemy.orm import Session

from app.models.victim import Victim


class VictimRepository:
    @staticmethod
    def get_by_id(db: Session, victim_id: uuid.UUID) -> Optional[Victim]:
        return db.query(Victim).filter(Victim.id == victim_id).first()

    @staticmethod
    def get_by_case_ref_id(db: Session, case_ref_id: str) -> Optional[Victim]:
        return db.query(Victim).filter(Victim.case_ref_id == case_ref_id.strip()).first()

    @staticmethod
    def create(db: Session, victim: Victim) -> Victim:
        db.add(victim)
        db.commit()
        db.refresh(victim)
        return victim

    @staticmethod
    def update(db: Session, victim: Victim) -> Victim:
        db.commit()
        db.refresh(victim)
        return victim
