import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.authority import Authority
from app.models.victim import Victim
from app.models.case import Case
from app.models.interaction import Interaction


@pytest.fixture
def seed_interaction_data(db_session: Session):
    # 1. Authority
    authority = Authority(
        id=uuid.uuid4(),
        role="district_official",
        jurisdiction_level="district",
        district="South Delhi",
        state="Delhi",
    )
    db_session.add(authority)

    # 2. Victim with ACTIVE consent
    active_victim = Victim(
        id=uuid.uuid4(),
        case_ref_id="POA-ACTIVE-001",
        preferred_language="hi",
        preferred_channel="sms",
        consent_status="active",
    )
    db_session.add(active_victim)

    active_case = Case(
        id=uuid.uuid4(),
        victim_id=active_victim.id,
        crime_category="harassment",
        legal_stage="investigation",
        assigned_authority_id=authority.id,
        status="active",
    )
    db_session.add(active_case)

    # 3. Victim with PENDING consent
    pending_victim = Victim(
        id=uuid.uuid4(),
        case_ref_id="POA-PENDING-002",
        preferred_language="hi",
        preferred_channel="chatbot",
        consent_status="pending",
    )
    db_session.add(pending_victim)

    pending_case = Case(
        id=uuid.uuid4(),
        victim_id=pending_victim.id,
        crime_category="threat",
        legal_stage="pre_trial",
        assigned_authority_id=authority.id,
        status="active",
    )
    db_session.add(pending_case)

    # 4. Victim with REVOKED consent
    revoked_victim = Victim(
        id=uuid.uuid4(),
        case_ref_id="POA-REVOKED-003",
        preferred_language="en",
        preferred_channel="app",
        consent_status="revoked",
    )
    db_session.add(revoked_victim)

    revoked_case = Case(
        id=uuid.uuid4(),
        victim_id=revoked_victim.id,
        crime_category="property_damage",
        legal_stage="trial",
        assigned_authority_id=authority.id,
        status="active",
    )
    db_session.add(revoked_case)

    db_session.commit()

    return {
        "active_case_id": active_case.id,
        "pending_case_id": pending_case.id,
        "revoked_case_id": revoked_case.id,
    }


def test_create_interaction_success(client: TestClient, db_session: Session, seed_interaction_data):
    case_id = seed_interaction_data["active_case_id"]
    response = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "chatbot",
            "response_text": "I am feeling very uneasy and anxious about the upcoming court hearing.",
            "response_latency_sec": 14,
            "was_skipped": False,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "occurred_at" in data

    # Verify DB persistence
    interaction = db_session.query(Interaction).filter(Interaction.id == uuid.UUID(data["id"])).first()
    assert interaction is not None
    assert interaction.case_id == case_id
    assert interaction.channel == "chatbot"
    assert interaction.response_latency_sec == 14
    assert interaction.raw_ref_pointer is not None
    assert interaction.raw_ref_pointer.startswith("vault://interactions/")


def test_create_interaction_skipped(client: TestClient, seed_interaction_data):
    case_id = seed_interaction_data["active_case_id"]
    response = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "sms",
            "response_text": None,
            "was_skipped": True,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data


def test_create_interaction_inactive_consent_pending(client: TestClient, seed_interaction_data):
    case_id = seed_interaction_data["pending_case_id"]
    response = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "chatbot",
            "response_text": "Hello, I wanted to talk.",
        },
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "CONSENT_INACTIVE"


def test_create_interaction_inactive_consent_revoked(client: TestClient, seed_interaction_data):
    case_id = seed_interaction_data["revoked_case_id"]
    response = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "app",
            "response_text": "Testing interaction",
        },
    )
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "CONSENT_INACTIVE"


def test_create_interaction_case_not_found(client: TestClient):
    random_id = str(uuid.uuid4())
    response = client.post(
        "/api/v1/interactions",
        json={
            "case_id": random_id,
            "channel": "chatbot",
            "response_text": "Testing with fake case ID",
        },
    )
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "CASE_NOT_FOUND"
