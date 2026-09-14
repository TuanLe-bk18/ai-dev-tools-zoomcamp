import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# In-memory SQLite for test isolation
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_empty_parties_list():
    response = client.get("/api/parties?status=active")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_parties():
    payload = {
        "name": "Sarah Connor",
        "party_size": 4,
        "phone": "555-0199",
        "notes": "Needs high chair",
    }
    response = client.post("/api/parties", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Sarah Connor"
    assert created["party_size"] == 4
    assert created["status"] == "waiting"
    assert "id" in created

    # Verify present in list
    list_resp = client.get("/api/parties?status=active")
    assert list_resp.status_code == 200
    parties = list_resp.json()
    assert len(parties) == 1
    assert parties[0]["name"] == "Sarah Connor"


def test_update_party_status_and_notes():
    # Create party
    create_resp = client.post(
        "/api/parties", json={"name": "David Miller", "party_size": 2}
    )
    party_id = create_resp.json()["id"]

    # Update to notified
    update_resp = client.patch(
        f"/api/parties/{party_id}",
        json={"status": "notified", "notes": "Guest texted at front desk"},
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["status"] == "notified"
    assert updated["notes"] == "Guest texted at front desk"

    # Update to seated
    seat_resp = client.patch(f"/api/parties/{party_id}", json={"status": "seated"})
    assert seat_resp.status_code == 200
    assert seat_resp.json()["status"] == "seated"

    # Verify not in active queue anymore
    active_resp = client.get("/api/parties?status=active")
    assert len(active_resp.json()) == 0

    # Verify appears in seated filter
    seated_resp = client.get("/api/parties?status=seated")
    assert len(seated_resp.json()) == 1


def test_delete_party():
    create_resp = client.post(
        "/api/parties", json={"name": "Elena Rostova", "party_size": 5}
    )
    party_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/parties/{party_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Party deleted"

    # Confirm 404 on second delete
    del_again = client.delete(f"/api/parties/{party_id}")
    assert del_again.status_code == 404
