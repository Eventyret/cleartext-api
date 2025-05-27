from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_summarize_endpoint():
    response = client.post(
        "/summarize/",
        json={"text": "FastAPI is a modern Python framework for building APIs."},
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "summary" in json_data
    assert "provider" in json_data


def test_summarize_invalid_length():
    response = client.post(
        "/summarize/", json={"text": "This is test text.", "length": "gigantic"}
    )
    assert response.status_code == 422
    json_data = response.json()
    assert "detail" in json_data


def test_summarize_missing_text():
    response = client.post("/summarize/", json={"length": "short"})
    assert response.status_code == 422
