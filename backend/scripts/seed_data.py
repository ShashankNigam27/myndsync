import sys
from pathlib import Path

# Ensure backend root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.authority import Authority
from app.models.user import User
from app.models.victim import Victim
from app.models.case import Case


def seed_data():
    db: Session = SessionLocal()
    try:
        print("[*] Seeding development data...")

        # 1. Check or create Authorities
        district_auth = (
            db.query(Authority)
            .filter(Authority.district == "South Delhi")
            .first()
        )
        if not district_auth:
            district_auth = Authority(
                id=uuid.uuid4(),
                role="district_official",
                jurisdiction_level="district",
                district="South Delhi",
                state="Delhi",
            )
            db.add(district_auth)
            db.commit()
            db.refresh(district_auth)
            print(f"Created Authority: {district_auth.district} ({district_auth.id})")

        state_auth = (
            db.query(Authority)
            .filter(Authority.jurisdiction_level == "state", Authority.state == "Delhi")
            .first()
        )
        if not state_auth:
            state_auth = Authority(
                id=uuid.uuid4(),
                role="state_authority",
                jurisdiction_level="state",
                district=None,
                state="Delhi",
            )
            db.add(state_auth)
            db.commit()
            db.refresh(state_auth)
            print(f"Created Authority: {state_auth.state} State ({state_auth.id})")

        # 2. Check or create Users
        users_to_seed = [
            {
                "email": "admin@myndsync.gov.in",
                "full_name": "System Administrator",
                "password": "Password123!",
                "role": "admin",
                "authority_id": None,
            },
            {
                "email": "district.officer@delhi.gov.in",
                "full_name": "Rajesh Kumar (District Officer)",
                "password": "Password123!",
                "role": "district_official",
                "authority_id": district_auth.id,
            },
            {
                "email": "counsellor.ananya@delhi.gov.in",
                "full_name": "Dr. Ananya Sharma (Counsellor)",
                "password": "Password123!",
                "role": "counsellor",
                "authority_id": district_auth.id,
            },
            {
                "email": "state.director@delhi.gov.in",
                "full_name": "Pooja Verma (State Director)",
                "password": "Password123!",
                "role": "state_authority",
                "authority_id": state_auth.id,
            },
        ]

        for u in users_to_seed:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if not existing:
                new_user = User(
                    id=uuid.uuid4(),
                    full_name=u["full_name"],
                    email=u["email"],
                    hashed_password=hash_password(u["password"]),
                    role=u["role"],
                    authority_id=u["authority_id"],
                    is_active=True,
                )
                db.add(new_user)
                print(f"Created User: {u['email']} [{u['role']}]")

        # 3. Check or create Sample Victims & Cases
        active_victim = db.query(Victim).filter(Victim.case_ref_id == "POA-2026-DEL-101").first()
        if not active_victim:
            active_victim = Victim(
                id=uuid.uuid4(),
                case_ref_id="POA-2026-DEL-101",
                preferred_language="hi",
                preferred_channel="chatbot",
                consent_status="active",
                enrolled_at=datetime.now(timezone.utc),
            )
            db.add(active_victim)
            db.commit()
            db.refresh(active_victim)
            print(f"Created Active Victim: {active_victim.case_ref_id} ({active_victim.id})")

        active_case = db.query(Case).filter(Case.victim_id == active_victim.id).first()
        if not active_case:
            active_case = Case(
                id=uuid.uuid4(),
                victim_id=active_victim.id,
                crime_category="caste_violence_intimidation",
                legal_stage="investigation",
                assigned_authority_id=district_auth.id,
                status="active",
            )
            db.add(active_case)
            db.commit()
            db.refresh(active_case)
            print(f"Created Case for Active Victim: {active_case.id}")

        pending_victim = db.query(Victim).filter(Victim.case_ref_id == "POA-2026-DEL-102").first()
        if not pending_victim:
            pending_victim = Victim(
                id=uuid.uuid4(),
                case_ref_id="POA-2026-DEL-102",
                preferred_language="hi",
                preferred_channel="sms",
                consent_status="pending",
                enrolled_at=datetime.now(timezone.utc),
            )
            db.add(pending_victim)
            db.commit()
            db.refresh(pending_victim)
            print(f"Created Pending Victim: {pending_victim.case_ref_id} ({pending_victim.id})")

        pending_case = db.query(Case).filter(Case.victim_id == pending_victim.id).first()
        if not pending_case:
            pending_case = Case(
                id=uuid.uuid4(),
                victim_id=pending_victim.id,
                crime_category="threat_witness",
                legal_stage="pre_trial",
                assigned_authority_id=district_auth.id,
                status="active",
            )
            db.add(pending_case)
            db.commit()
            db.refresh(pending_case)
            print(f"Created Case for Pending Victim: {pending_case.id}")

        db.commit()
        print("[+] Development data seed completed successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
