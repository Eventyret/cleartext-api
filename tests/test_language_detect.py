from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


def test_language_detect_success():
    with patch("app.api.endpoints.language_detect.detect_language", return_value="fr"):
        response = client.post(
            "/language-detect/", json={"text": "Bonjour tout le monde"}
        )
        assert response.status_code == 200
        assert response.json()["language"] == "fr"


def test_language_detect_empty():
    response = client.post("/language-detect/", json={"text": ""})
    assert response.status_code == 422


def test_language_detect_spaces_only():
    response = client.post("/language-detect/", json={"text": "     "})
    assert response.status_code == 422


def test_language_detect_unknown_language():
    with patch(
        "app.api.endpoints.language_detect.detect_language", return_value="unknown"
    ):
        response = client.post("/language-detect/", json={"text": "asdfghjkl"})
        assert response.status_code == 422
        assert "Could not determine language" in response.json()["detail"]
