import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.interaction import InteractionCreate, InteractionResponse
from app.schemas.assessment import AssessmentResponse
from app.services.interaction_service import InteractionService

router = APIRouter(prefix="/interactions", tags=["Interactions & Check-ins"])


@router.post(
    "",
    response_model=InteractionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record Check-in Interaction (with Automatic NLP Assessment)",
)
async def create_interaction(
    interaction_in: InteractionCreate,
    db: Session = Depends(get_db),
) -> InteractionResponse:
    """Record a check-in interaction response from a victim channel. Requires active consent. Automatically triggers NLP sentiment analysis and generates an Assessment record."""
    return InteractionService.create_interaction(db, interaction_in)


@router.get(
    "/{interaction_id}/assessment",
    response_model=AssessmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Assessment for an Interaction",
)
async def get_interaction_assessment(
    interaction_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> AssessmentResponse:
    """Retrieve the AI assessment signals (sentiment_score, confidence, etc.) computed for a specific interaction."""
    return InteractionService.get_assessment_by_interaction_id(db, interaction_id)
