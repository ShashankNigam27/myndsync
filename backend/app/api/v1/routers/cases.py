import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.distress_score import CaseDistressHistoryResponse
from app.services.case_service import CaseService

router = APIRouter(prefix="/cases", tags=["Cases & Risk Management"])


@router.get(
    "/{case_id}/distress-history",
    response_model=CaseDistressHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Case Distress Score History (DDS Snapshots, Baseline & Trend)",
)
async def get_case_distress_history(
    case_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> CaseDistressHistoryResponse:
    """Retrieve full Dynamic Distress Score (DDS) history for a case, including baseline score, trend slope, and categorized risk band per check-in."""
    return CaseService.get_case_distress_history(db, case_id)
