import uuid
from sqlalchemy.orm import Session
from app.models.authority import Authority
from app.models.user import User
from app.models.victim import Victim
from app.models.case import Case
from app.models.interaction import Interaction
from app.models.assessment import Assessment
from app.models.distress_score import DistressScore


def test_models_and_relationships(db_session: Session):
    # 1. Create Authority
    authority = Authority(
        role="district_official",
        jurisdiction_level="district",
        district="Central Delhi",
        state="Delhi",
    )
    db_session.add(authority)
    db_session.commit()
    db_session.refresh(authority)

    assert authority.id is not None
    assert authority.district == "Central Delhi"

    # 2. Create User linked to Authority
    user = User(
        full_name="Rajesh Kumar",
        email="rajesh.kumar@example.gov.in",
        hashed_password="mockhashedpassword123",
        role="district_official",
        authority_id=authority.id,
        auth_provider="local",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.authority.district == "Central Delhi"
    assert len(authority.users) == 1

    # 3. Create Victim
    victim = Victim(
        case_ref_id="CASE-2026-DEL-001",
        preferred_language="hi",
        preferred_channel="sms",
        consent_status="active",
    )
    db_session.add(victim)
    db_session.commit()
    db_session.refresh(victim)

    assert victim.id is not None
    assert victim.case_ref_id == "CASE-2026-DEL-001"

    # 4. Create Case linked to Victim and Authority
    case = Case(
        victim_id=victim.id,
        crime_category="atrocity_threat",
        legal_stage="investigation",
        assigned_authority_id=authority.id,
        status="active",
    )
    db_session.add(case)
    db_session.commit()
    db_session.refresh(case)

    assert case.id is not None
    assert case.victim.case_ref_id == "CASE-2026-DEL-001"
    assert case.assigned_authority.district == "Central Delhi"
    assert len(victim.cases) == 1
    assert len(authority.assigned_cases) == 1

    # 5. Create Interaction linked to Case
    interaction = Interaction(
        case_id=case.id,
        channel="chatbot",
        raw_ref_pointer="vault://interactions/sample-pointer-123",
        response_latency_sec=10,
        was_skipped=False,
    )
    db_session.add(interaction)
    db_session.commit()
    db_session.refresh(interaction)

    assert interaction.id is not None
    assert interaction.case_id == case.id
    assert len(case.interactions) == 1
    assert case.interactions[0].raw_ref_pointer == "vault://interactions/sample-pointer-123"

    # 6. Create Assessment linked to Interaction
    assessment = Assessment(
        interaction_id=interaction.id,
        sentiment_score=-0.5,
        confidence=0.85,
    )
    db_session.add(assessment)
    db_session.commit()
    db_session.refresh(assessment)

    assert assessment.id is not None
    assert interaction.assessment.sentiment_score == -0.5

    # 7. Create DistressScore linked to Case and Assessment
    distress_score = DistressScore(
        case_id=case.id,
        assessment_id=assessment.id,
        current_score=65.0,
        baseline_score=45.0,
        trend_slope=20.0,
        risk_band="high",
    )
    db_session.add(distress_score)
    db_session.commit()
    db_session.refresh(distress_score)

    assert distress_score.id is not None
    assert distress_score.risk_band == "high"
    assert len(case.distress_scores) == 1
    assert assessment.distress_score.current_score == 65.0
