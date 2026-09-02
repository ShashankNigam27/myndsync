import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.ai.nlp.sentiment import SentimentAnalyzer
from app.models.authority import Authority
from app.models.victim import Victim
from app.models.case import Case
from app.models.interaction import Interaction
from app.models.assessment import Assessment


def test_sentiment_analyzer_unit():
    analyzer = SentimentAnalyzer()

    # 1. Severe distress (English)
    res_distress = analyzer.analyze("I am terrified and hopeless, they gave me a death threat.")
    assert res_distress.sentiment_score < -0.3
    assert res_distress.confidence >= 0.7

    # 2. Positive / safe (English)
    res_pos = analyzer.analyze("I am feeling very safe, peaceful, and supported today.")
    assert res_pos.sentiment_score > 0.3

    # 3. Hindi distress (Devanagari)
    res_hindi = analyzer.analyze("मुझे बहुत डर लग रहा है और बहुत चिंता हो रही है।")
    assert res_hindi.sentiment_score < 0.0

    # 4. Hinglish distress
    res_hinglish = analyzer.analyze("Mujhe bohot darr lag raha hai, dhamki mili hai.")
    assert res_hinglish.sentiment_score < 0.0

    # 5. Empty / neutral
    res_empty = analyzer.analyze("")
    assert res_empty.sentiment_score == 0.0
    assert res_empty.confidence == 0.5


@pytest.fixture
def seed_assessment_case(db_session: Session):
    authority = Authority(
        id=uuid.uuid4(),
        role="district_official",
        jurisdiction_level="district",
        district="South Delhi",
        state="Delhi",
    )
    db_session.add(authority)

    victim = Victim(
        id=uuid.uuid4(),
        case_ref_id="POA-ASSESS-001",
        preferred_language="hi",
        preferred_channel="chatbot",
        consent_status="active",
    )
    db_session.add(victim)

    case = Case(
        id=uuid.uuid4(),
        victim_id=victim.id,
        crime_category="intimidation",
        legal_stage="investigation",
        assigned_authority_id=authority.id,
        status="active",
    )
    db_session.add(case)
    db_session.commit()

    return {"case_id": case.id, "victim_id": victim.id}


def test_automatic_assessment_creation_and_retrieval(client: TestClient, db_session: Session, seed_assessment_case):
    case_id = seed_assessment_case["case_id"]

    # 1. Post an interaction with distress text
    create_res = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "chatbot",
            "response_text": "I am feeling scared and anxious because people are following me.",
            "response_latency_sec": 15,
            "was_skipped": False,
        },
    )
    assert create_res.status_code == 201
    interaction_id = create_res.json()["id"]

    # 2. Retrieve the assessment via GET /api/v1/interactions/{id}/assessment
    get_res = client.get(f"/api/v1/interactions/{interaction_id}/assessment")
    assert get_res.status_code == 200
    assessment_data = get_res.json()

    assert assessment_data["interaction_id"] == interaction_id
    assert assessment_data["sentiment_score"] < 0.0  # Detected distress
    assert 0.0 <= assessment_data["confidence"] <= 1.0
    assert "processed_at" in assessment_data

    # 3. Direct DB check
    db_assessment = (
        db_session.query(Assessment)
        .filter(Assessment.interaction_id == uuid.UUID(interaction_id))
        .first()
    )
    assert db_assessment is not None
    assert db_assessment.sentiment_score == assessment_data["sentiment_score"]


def test_get_assessment_not_found(client: TestClient):
    random_id = str(uuid.uuid4())
    res = client.get(f"/api/v1/interactions/{random_id}/assessment")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "INTERACTION_NOT_FOUND"
