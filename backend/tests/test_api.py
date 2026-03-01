import sys
import pytest
from fastapi.testclient import TestClient
from backend import storage
from backend.main import app
import os
import tempfile
import json

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_data(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_dir:
        storage.DATA_DIR = temp_dir
        user_dir = os.path.join(temp_dir, "mock-user-id")
        os.makedirs(user_dir)
        
        config = {
            "email": "test@example.com",
            "subscriptions": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Tech",
                    "prompt": "AI stuff",
                    "frequency": "DAILY"
                }
            ]
        }
        with open(os.path.join(user_dir, "config.json"), "w") as f:
            json.dump(config, f)
            
        history = [
            {
                "id": "email-1",
                "sub_id": "123e4567-e89b-12d3-a456-426614174000",
                "subject": "AI Daily",
                "sent_at": "2023-10-27T10:00:00Z",
                "html_content": "<p>Hello</p>",
                "text_content": "Hello"
            }
        ]
        with open(os.path.join(user_dir, "history_email.json"), "w") as f:
            json.dump(history, f)
            
        yield temp_dir

def test_get_config():
    response = client.get("/api/v1/config")
    assert response.status_code == 200
    data = response.json()
    assert len(data["subscriptions"]) == 1
    assert data["subscriptions"][0]["name"] == "Tech"

def test_update_config():
    payload = {
        "subscriptions": [
            {
                "id": "abc-uuid",
                "name": "Space",
                "prompt": "NASA",
                "frequency": "WEEKLY"
            }
        ]
    }
    response = client.put("/api/v1/config", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["subscriptions"]) == 1
    assert data["subscriptions"][0]["name"] == "Space"

def test_list_history_email():
    response = client.get("/api/v1/history_email?user_id=mock-user-id&start_date=2023-10-01T00:00:00Z&end_date=2023-10-31T23:59:59Z")
    assert response.status_code == 200
    assert len(response.json()["emails"]) == 1
    assert response.json()["emails"][0]["id"] == "email-1"

def test_read_history_email():
    response = client.get("/api/v1/history_email/email-1?user_id=mock-user-id")
    assert response.status_code == 200
    assert response.json()["subject"] == "AI Daily"

if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv))
