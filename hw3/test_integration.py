"""Integration test for two-agent task exchange flow (Homework 3 Question 2)."""

from fastapi.testclient import TestClient
import pytest

import main
from database import Base, engine


@pytest.fixture(autouse=True)
def empty_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_two_agents_exchange_task_and_result():
    with TestClient(main.app) as client:
        # 1. Register sender (Alice)
        alice_resp = client.post("/api/v1/agents", json={"name": "alice", "description": "Sender agent"})
        assert alice_resp.status_code == 201
        alice = alice_resp.json()
        alice_token = alice["token"]
        alice_headers = {"Authorization": f"Bearer {alice_token}"}

        # 2. Register recipient (Bob / Uppercase worker)
        bob_resp = client.post("/api/v1/agents", json={"name": "bob", "description": "Uppercase processor"})
        assert bob_resp.status_code == 201
        bob = bob_resp.json()
        bob_token = bob["token"]
        bob_headers = {"Authorization": f"Bearer {bob_token}"}

        # 3. Alice sends a task to Bob
        task_input = "convert this to uppercase"
        create_task_resp = client.post(
            "/api/v1/tasks",
            headers=alice_headers,
            json={"to": bob["agent_id"], "input": task_input},
        )
        assert create_task_resp.status_code == 201
        task_data = create_task_resp.json()
        task_id = task_data["task_id"]
        assert task_data["status"] == "queued"

        # 4. Bob claims the task
        claim_resp = client.post(
            "/api/v1/tasks/claim",
            headers=bob_headers,
            json={"worker_id": "bob-worker-1", "wait_seconds": 0},
        )
        assert claim_resp.status_code == 200
        claim_data = claim_resp.json()
        assert claim_data["task_id"] == task_id
        assert claim_data["input"] == task_input
        claim_token = claim_data["claim_token"]

        # 5. Bob processes and completes the task
        completed_output = task_input.upper()
        complete_resp = client.post(
            f"/api/v1/tasks/{task_id}/complete",
            headers=bob_headers,
            json={"claim_token": claim_token, "output": completed_output},
        )
        assert complete_resp.status_code == 200
        assert complete_resp.json()["status"] == "completed"

        # 6. Alice retrieves task details and verifies final status is 'completed'
        get_task_resp = client.get(f"/api/v1/tasks/{task_id}", headers=alice_headers)
        assert get_task_resp.status_code == 200
        final_task = get_task_resp.json()

        # Verification for Question 2
        assert final_task["status"] == "completed"
        assert final_task["output"] == completed_output
