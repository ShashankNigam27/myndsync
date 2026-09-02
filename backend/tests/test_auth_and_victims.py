import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.authority import Authority
from app.models.user import User
from app.models.victim import Victim


@pytest.fixture
def seed_auth_data(db_session: Session):
    authority = Authority(
        id=uuid.uuid4(),
        role="district_official",
        jurisdiction_level="district",
        district="South Delhi",
        state="Delhi",
    )
    db_session.add(authority)

    district_user = User(
        id=uuid.uuid4(),
        full_name="District Officer",
        email="officer@delhi.gov.in",
        hashed_password=hash_password("securepassword123"),
        role="district_official",
        authority_id=authority.id,
        is_active=True,
    )
    db_session.add(district_user)

    counsellor_user = User(
        id=uuid.uuid4(),
        full_name="Counsellor Ananya",
        email="ananya.counsellor@delhi.gov.in",
        hashed_password=hash_password("securepassword123"),
        role="counsellor",
        authority_id=authority.id,
        is_active=True,
    )
    db_session.add(counsellor_user)

    db_session.commit()
    return {"authority": authority, "district_user": district_user, "counsellor_user": counsellor_user}


def test_login_success(client: TestClient, seed_auth_data):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "officer@delhi.gov.in", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["role"] == "district_official"


def test_oauth2_token_form_success(client: TestClient, seed_auth_data):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "officer@delhi.gov.in", "password": "securepassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, seed_auth_data):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "officer@delhi.gov.in", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "INVALID_CREDENTIALS"


def test_refresh_token_flow(client: TestClient, seed_auth_data):
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "officer@delhi.gov.in", "password": "securepassword123"},
    )
    refresh_token = login_res.json()["refresh_token"]

    refresh_res = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_res.status_code == 200
    assert "access_token" in refresh_res.json()


def test_get_me_authenticated(client: TestClient, seed_auth_data):
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "officer@delhi.gov.in", "password": "securepassword123"},
    )
    token = login_res.json()["access_token"]

    me_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "officer@delhi.gov.in"
    assert me_res.json()["role"] == "district_official"


def test_enroll_victim_success_and_duplicate_handling(client: TestClient, seed_auth_data):
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "officer@delhi.gov.in", "password": "securepassword123"},
    )
    token = login_res.json()["access_token"]

    enroll_res = client.post(
        "/api/v1/victims",
        json={
            "case_ref_id": "POA-2026-DEL-101",
            "preferred_language": "hi",
            "preferred_channel": "sms",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert enroll_res.status_code == 201
    victim_data = enroll_res.json()
    assert "id" in victim_data
    assert victim_data["case_ref_id"] == "POA-2026-DEL-101"
    assert "enrolled_at" in victim_data

    dup_res = client.post(
        "/api/v1/victims",
        json={
            "case_ref_id": "POA-2026-DEL-101",
            "preferred_language": "hi",
            "preferred_channel": "sms",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert dup_res.status_code == 409
    assert dup_res.json()["error"]["code"] == "VICTIM_ALREADY_ENROLLED"


def test_enroll_victim_role_forbidden(client: TestClient, seed_auth_data):
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "ananya.counsellor@delhi.gov.in", "password": "securepassword123"},
    )
    token = login_res.json()["access_token"]

    enroll_res = client.post(
        "/api/v1/victims",
        json={
            "case_ref_id": "POA-2026-DEL-102",
            "preferred_language": "hi",
            "preferred_channel": "sms",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert enroll_res.status_code == 403
    assert enroll_res.json()["error"]["code"] == "FORBIDDEN_ROLE"


def test_record_consent_flow(client: TestClient, seed_auth_data):
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "officer@delhi.gov.in", "password": "securepassword123"},
    )
    token = login_res.json()["access_token"]

    enroll_res = client.post(
        "/api/v1/victims",
        json={
            "case_ref_id": "POA-2026-DEL-103",
            "preferred_language": "hi",
            "preferred_channel": "sms",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    victim_id = enroll_res.json()["id"]

    consent_res = client.post(
        "/api/v1/consents",
        json={
            "victim_id": victim_id,
            "consented": True,
            "channels": ["sms", "chatbot"],
        },
    )
    assert consent_res.status_code == 201
    assert consent_res.json()["status"] == "active"
    assert consent_res.json()["victim_id"] == victim_id

    revoke_res = client.post(
        "/api/v1/consents",
        json={
            "victim_id": victim_id,
            "consented": False,
            "channels": [],
        },
    )
    assert revoke_res.status_code == 201
    assert revoke_res.json()["status"] == "revoked"


def test_record_consent_nonexistent_victim(client: TestClient):
    fake_id = str(uuid.uuid4())
    res = client.post(
        "/api/v1/consents",
        json={
            "victim_id": fake_id,
            "consented": True,
            "channels": ["sms"],
        },
    )
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "VICTIM_NOT_FOUND"


def test_record_consent_empty_channels_when_consenting(client: TestClient, seed_auth_data):
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "officer@delhi.gov.in", "password": "securepassword123"},
    )
    token = login_res.json()["access_token"]

    enroll_res = client.post(
        "/api/v1/victims",
        json={
            "case_ref_id": "POA-2026-DEL-104",
            "preferred_language": "hi",
            "preferred_channel": "sms",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    victim_id = enroll_res.json()["id"]

    res = client.post(
        "/api/v1/consents",
        json={
            "victim_id": victim_id,
            "consented": True,
            "channels": [],
        },
    )
    assert res.status_code == 400
    assert res.json()["error"]["code"] == "CHANNELS_REQUIRED"
