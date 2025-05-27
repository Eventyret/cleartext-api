from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_rewrite_endpoint():
    with patch(
        "app.api.endpoints.rewrite.rewrite",
        return_value={"rewritten": "Can you help me?", "provider": "mock"},
    ):
        response = client.post(
            "/rewrite/",
            json={"text": "Could you provide me with assistance?", "style": "simple"},
        )
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["rewritten"] == "Can you help me?"
        assert json_data["provider"] == "mock"


def test_rewrite_invalid_style():
    response = client.post(
        "/rewrite/",
        json={"text": "Let's rewrite this.", "style": "ye olde medieval"},
    )
    assert response.status_code == 422
    json_data = response.json()
    assert "detail" in json_data


def test_rewrite_missing_text():
    response = client.post(
        "/rewrite/",
        json={"style": "simple"},
    )
    assert response.status_code == 422
