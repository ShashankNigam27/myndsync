import uuid
from typing import List
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.repositories.case_repository import CaseRepository
from app.repositories.distress_score_repository import DistressScoreRepository
from app.schemas.distress_score import (
    DistressScoreResponse,
    CaseDistressHistoryResponse,
)


class CaseService:
    @staticmethod
    def get_case_distress_history(
        db: Session, case_id: uuid.UUID
    ) -> CaseDistressHistoryResponse:
        case = CaseRepository.get_by_id(db, case_id)
        if not case:
            raise NotFoundException(
                message=f"Case with ID '{case_id}' not found",
                code="CASE_NOT_FOUND",
                details={"case_id": str(case_id)},
            )

        history_records = DistressScoreRepository.get_history_by_case_id(db, case_id)
        history_responses = [
            DistressScoreResponse.model_validate(record) for record in history_records
        ]

        latest = history_records[-1] if history_records else None
        first = history_records[0] if history_records else None

        return CaseDistressHistoryResponse(
            case_id=case_id,
            total_checkins=len(history_records),
            current_score=latest.current_score if latest else None,
            current_risk_band=latest.risk_band if latest else None,
            baseline_score=first.baseline_score if first else None,
            trend_slope=latest.trend_slope if latest else None,
            history=history_responses,
        )
