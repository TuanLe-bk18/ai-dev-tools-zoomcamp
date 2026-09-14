import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_parties():
    response = client.get("/api/parties?status=active")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_create_party():
    payload = {
        "name": "Bruce Wayne",
        "party_size": 3,
        "phone": "555-9999",
        "notes": "Quiet corner",
    }
    response = client.post("/api/parties", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Bruce Wayne"
    assert created["party_size"] == 3
    assert created["status"] == "waiting"
    assert "id" in created


def test_update_party_status():
    # Update party 1 status to seated
    response = client.patch("/api/parties/1", json={"status": "seated"})
    assert response.status_code == 200
    updated = response.json()
    assert updated["id"] == 1
    assert updated["status"] == "seated"


def test_delete_party():
    response = client.delete("/api/parties/2")
    assert response.status_code == 200
    assert response.json()["message"] == "Party deleted"

    # Confirm 404 on subsequent delete
    not_found_resp = client.delete("/api/parties/2")
    assert not_found_resp.status_code == 404
