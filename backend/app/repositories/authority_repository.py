import uuid
from typing import Optional
from sqlalchemy.orm import Session

from app.models.authority import Authority


class AuthorityRepository:
    @staticmethod
    def get_by_id(db: Session, authority_id: uuid.UUID) -> Optional[Authority]:
        return db.query(Authority).filter(Authority.id == authority_id).first()

    @staticmethod
    def create(db: Session, authority: Authority) -> Authority:
        db.add(authority)
        db.commit()
        db.refresh(authority)
        return authority
