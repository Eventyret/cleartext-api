from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rewrite_endpoint():
    response = client.post(
        "/rewrite/",
        json={"text": "Could you provide me with assistance?", "style": "simple"},
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "rewritten" in json_data
    assert "provider" in json_data


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
