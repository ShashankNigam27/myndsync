import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.ai.scoring.dds import DynamicDistressScorer
from app.models.authority import Authority
from app.models.victim import Victim
from app.models.case import Case
from app.models.distress_score import DistressScore


def test_dds_scorer_unit_components():
    scorer = DynamicDistressScorer()

    # 1. Extreme distress sentiment (-1.0) with low latency
    score_distress = scorer.compute_score(
        sentiment_score=-1.0,
        was_skipped=False,
        response_latency_sec=10,
    )
    # High distress score
    assert score_distress >= 60.0

    # 2. Positive / peaceful sentiment (+1.0) with fast response
    score_peace = scorer.compute_score(
        sentiment_score=1.0,
        was_skipped=False,
        response_latency_sec=5,
    )
    # Low distress score
    assert score_peace <= 30.0

    # 3. Skipped check-in penalty
    score_skipped = scorer.compute_score(
        sentiment_score=0.0,
        was_skipped=True,
    )
    # Skipped increases engagement component to 80.0
    assert score_skipped > 50.0


def test_risk_band_assignment_thresholds():
    scorer = DynamicDistressScorer()

    assert scorer.determine_risk_band(15.0) == "low"
    assert scorer.determine_risk_band(39.9) == "low"
    assert scorer.determine_risk_band(40.0) == "moderate"
    assert scorer.determine_risk_band(59.9) == "moderate"
    assert scorer.determine_risk_band(60.0) == "high"
    assert scorer.determine_risk_band(79.9) == "high"
    assert scorer.determine_risk_band(80.0) == "critical"
    assert scorer.determine_risk_band(95.0) == "critical"
    # Safety keyword override
    assert scorer.determine_risk_band(25.0, safety_keyword_flag=True) == "critical"


def test_trend_slope_calculation():
    scorer = DynamicDistressScorer()

    # Single score -> 0 slope
    assert scorer.calculate_trend_slope([], 30.0) == 0.0

    # Worsening distress sequence
    slope_worsening = scorer.calculate_trend_slope([20.0, 40.0], 60.0)
    assert slope_worsening == 20.0  # +20 points per check-in

    # Improving distress sequence
    slope_improving = scorer.calculate_trend_slope([80.0, 60.0], 40.0)
    assert slope_improving == -20.0  # -20 points per check-in


@pytest.fixture
def seed_case_for_scoring(db_session: Session):
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
        case_ref_id="POA-SCORE-001",
        preferred_language="hi",
        preferred_channel="chatbot",
        consent_status="active",
    )
    db_session.add(victim)

    case = Case(
        id=uuid.uuid4(),
        victim_id=victim.id,
        crime_category="threat_intimidation",
        legal_stage="investigation",
        assigned_authority_id=authority.id,
        status="active",
    )
    db_session.add(case)
    db_session.commit()

    return {"case_id": case.id}


def test_distress_score_progression_and_history_endpoint(
    client: TestClient, db_session: Session, seed_case_for_scoring
):
    case_id = seed_case_for_scoring["case_id"]

    # 1. First check-in: Calm / Positive (establishes baseline)
    res1 = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "chatbot",
            "response_text": "Everything is fine and safe today, thank you.",
            "response_latency_sec": 8,
            "was_skipped": False,
        },
    )
    assert res1.status_code == 201

    # Check history endpoint after 1st check-in
    history_res1 = client.get(f"/api/v1/cases/{case_id}/distress-history")
    assert history_res1.status_code == 200
    data1 = history_res1.json()
    assert data1["total_checkins"] == 1
    assert data1["current_risk_band"] == "low"
    baseline = data1["baseline_score"]
    assert baseline is not None
    assert data1["trend_slope"] == 0.0

    # 2. Second check-in: Mild anxiety
    res2 = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "chatbot",
            "response_text": "I feel a bit worried and uneasy about the situation.",
            "response_latency_sec": 20,
            "was_skipped": False,
        },
    )
    assert res2.status_code == 201

    # 3. Third check-in: Severe distress & threat
    res3 = client.post(
        "/api/v1/interactions",
        json={
            "case_id": str(case_id),
            "channel": "chatbot",
            "response_text": "They came again and gave me a death threat, I am terrified and hopeless!",
            "response_latency_sec": 35,
            "was_skipped": False,
        },
    )
    assert res3.status_code == 201

    # Check full distress history endpoint
    history_res3 = client.get(f"/api/v1/cases/{case_id}/distress-history")
    assert history_res3.status_code == 200
    data3 = history_res3.json()

    assert data3["case_id"] == str(case_id)
    assert data3["total_checkins"] == 3
    # Baseline remains the first score
    assert data3["baseline_score"] == baseline
    # Worsening trend slope
    assert data3["trend_slope"] > 0.0
    # Current risk band escalated to high or critical
    assert data3["current_risk_band"] in ["high", "critical"]
    assert len(data3["history"]) == 3
    assert data3["history"][0]["baseline_score"] == baseline
    assert data3["history"][2]["current_score"] > data3["history"][0]["current_score"]


def test_get_case_distress_history_not_found(client: TestClient):
    fake_case_id = str(uuid.uuid4())
    res = client.get(f"/api/v1/cases/{fake_case_id}/distress-history")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "CASE_NOT_FOUND"
