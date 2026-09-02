from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.db.session import get_db
from app.models.user import User
from app.schemas.victim import (
    VictimCreate,
    VictimResponse,
    ConsentCreate,
    ConsentResponse,
)
from app.services.victim_service import VictimService

router = APIRouter(tags=["Victims & Consent"])


@router.post(
    "/victims",
    response_model=VictimResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register/Enroll Victim Case",
)
async def enroll_victim(
    victim_in: VictimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("district_official", "admin")),
) -> VictimResponse:
    """Enroll a victim/witness into the monitoring system with their preferred channel and language. Authorized: District Official, Admin, System."""
    return VictimService.enroll_victim(db, victim_in)


@router.post(
    "/consents",
    response_model=ConsentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record or Update Victim Consent",
)
async def record_consent(
    consent_in: ConsentCreate,
    db: Session = Depends(get_db),
) -> ConsentResponse:
    """Record victim consent or revocation for periodic distress monitoring."""
    return VictimService.record_consent(db, consent_in)
