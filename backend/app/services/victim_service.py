from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, NotFoundException, BadRequestException
from app.models.victim import Victim
from app.repositories.victim_repository import VictimRepository
from app.schemas.victim import VictimCreate, VictimResponse, ConsentCreate, ConsentResponse


class VictimService:
    @staticmethod
    def enroll_victim(db: Session, data: VictimCreate) -> VictimResponse:
        case_ref = data.case_ref_id.strip()
        if not case_ref:
            raise BadRequestException(
                message="Case reference ID cannot be empty",
                code="INVALID_CASE_REF_ID",
            )

        existing = VictimRepository.get_by_case_ref_id(db, case_ref)
        if existing:
            raise ConflictException(
                message=f"Victim associated with case reference '{case_ref}' is already enrolled",
                code="VICTIM_ALREADY_ENROLLED",
                details={"case_ref_id": case_ref},
            )

        victim = Victim(
            case_ref_id=case_ref,
            preferred_language=data.preferred_language,
            preferred_channel=data.preferred_channel,
            consent_status="pending",
            enrolled_at=datetime.now(timezone.utc),
        )
        created = VictimRepository.create(db, victim)
        return VictimResponse.model_validate(created)

    @staticmethod
    def record_consent(db: Session, data: ConsentCreate) -> ConsentResponse:
        victim = VictimRepository.get_by_id(db, data.victim_id)
        if not victim:
            raise NotFoundException(
                message=f"Victim with ID '{data.victim_id}' not found",
                code="VICTIM_NOT_FOUND",
                details={"victim_id": str(data.victim_id)},
            )

        if data.consented:
            if not data.channels:
                raise BadRequestException(
                    message="At least one communication channel must be selected when consenting",
                    code="CHANNELS_REQUIRED",
                )
            victim.consent_status = "active"
            victim.preferred_channel = data.channels[0]
        else:
            victim.consent_status = "revoked"

        updated = VictimRepository.update(db, victim)
        return ConsentResponse(
            id=updated.id,
            victim_id=updated.id,
            status=updated.consent_status,
        )
