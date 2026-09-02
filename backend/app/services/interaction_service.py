import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.ai.nlp.sentiment import sentiment_analyzer
from app.ai.scoring.dds import distress_scorer
from app.core.exceptions import NotFoundException, ForbiddenException
from app.models.interaction import Interaction
from app.models.assessment import Assessment
from app.models.distress_score import DistressScore
from app.repositories.case_repository import CaseRepository
from app.repositories.victim_repository import VictimRepository
from app.repositories.interaction_repository import InteractionRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.distress_score_repository import DistressScoreRepository
from app.schemas.interaction import InteractionCreate, InteractionResponse
from app.schemas.assessment import AssessmentResponse


class InteractionService:
    @staticmethod
    def create_interaction(db: Session, data: InteractionCreate) -> InteractionResponse:
        # 1. Validate Case exists
        case = CaseRepository.get_by_id(db, data.case_id)
        if not case:
            raise NotFoundException(
                message=f"Case with ID '{data.case_id}' not found",
                code="CASE_NOT_FOUND",
                details={"case_id": str(data.case_id)},
            )

        # 2. Validate Victim active consent (Section 20 error handling rule)
        victim = case.victim
        if not victim:
            victim = VictimRepository.get_by_id(db, case.victim_id)

        if not victim or victim.consent_status != "active":
            raise ForbiddenException(
                message="Consent is inactive or missing for this victim. Interaction cannot be recorded.",
                code="CONSENT_INACTIVE",
                details={
                    "victim_id": str(case.victim_id),
                    "consent_status": victim.consent_status if victim else "missing",
                },
            )

        # 3. Simulate secure vault reference pointer for raw response (Section 10 & 19)
        raw_ref_pointer = None
        if data.response_text:
            raw_ref_pointer = f"vault://interactions/{uuid.uuid4()}"

        # 4. Create and persist interaction record
        now = datetime.now(timezone.utc)
        interaction = Interaction(
            case_id=case.id,
            channel=data.channel,
            raw_ref_pointer=raw_ref_pointer,
            response_latency_sec=data.response_latency_sec,
            was_skipped=data.was_skipped,
            occurred_at=now,
        )
        created_interaction = InteractionRepository.create(db, interaction)

        # 5. Phase 3: Automatically analyze NLP sentiment and create Assessment (Section 10 & 14)
        if data.was_skipped or not data.response_text:
            sentiment_score = 0.0
            confidence = 0.5
        else:
            sentiment_res = sentiment_analyzer.analyze(data.response_text)
            sentiment_score = sentiment_res.sentiment_score
            confidence = sentiment_res.confidence

        assessment = Assessment(
            interaction_id=created_interaction.id,
            sentiment_score=sentiment_score,
            confidence=confidence,
            processed_at=datetime.now(timezone.utc),
        )
        created_assessment = AssessmentRepository.create(db, assessment)

        # 6. Phase 4: Dynamic Distress Score (DDS) calculation (Section 15)
        # Compute instantaneous DDS score
        current_dds = distress_scorer.compute_score(
            sentiment_score=sentiment_score,
            was_skipped=data.was_skipped,
            response_latency_sec=data.response_latency_sec,
            emotion_label=assessment.emotion_label,
            voice_stress_score=assessment.voice_stress_score,
        )

        # Retrieve prior DDS history for baseline and trend slope computation
        past_history = DistressScoreRepository.get_history_by_case_id(db, case.id)
        past_scores = [record.current_score for record in past_history]

        if not past_scores:
            baseline_score = current_dds
        else:
            baseline_score = past_scores[0]  # First assessment DDS establishes personalized baseline

        trend_slope = distress_scorer.calculate_trend_slope(past_scores, current_dds)
        risk_band = distress_scorer.determine_risk_band(current_dds)

        distress_score_record = DistressScore(
            case_id=case.id,
            assessment_id=created_assessment.id,
            current_score=current_dds,
            baseline_score=baseline_score,
            trend_slope=trend_slope,
            risk_band=risk_band,
            computed_at=datetime.now(timezone.utc),
        )
        DistressScoreRepository.create(db, distress_score_record)

        return InteractionResponse.model_validate(created_interaction)

    @staticmethod
    def get_assessment_by_interaction_id(
        db: Session, interaction_id: uuid.UUID
    ) -> AssessmentResponse:
        # Check interaction exists
        interaction = InteractionRepository.get_by_id(db, interaction_id)
        if not interaction:
            raise NotFoundException(
                message=f"Interaction with ID '{interaction_id}' not found",
                code="INTERACTION_NOT_FOUND",
                details={"interaction_id": str(interaction_id)},
            )

        assessment = AssessmentRepository.get_by_interaction_id(db, interaction_id)
        if not assessment:
            raise NotFoundException(
                message=f"Assessment for interaction '{interaction_id}' has not been processed yet",
                code="ASSESSMENT_NOT_FOUND",
                details={"interaction_id": str(interaction_id)},
            )

        return AssessmentResponse.model_validate(assessment)
