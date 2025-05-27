from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_language_detect_success():
    response = client.post("/language-detect/", json={"text": "Bonjour tout le monde"})
    assert response.status_code == 200
    assert response.json()["language"] == "fr"


def test_language_detect_empty():
    response = client.post("/language-detect/", json={"text": ""})
    assert response.status_code == 422


def test_language_detect_spaces_only():
    response = client.post("/language-detect/", json={"text": "     "})
    assert response.status_code == 422


def test_language_detect_unknown_language():
    response = client.post("/language-detect/", json={"text": "asdfghjkl"})
    assert response.status_code == 422
    assert "Could not determine language" in response.json()["detail"]
