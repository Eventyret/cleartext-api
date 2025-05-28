from unittest.mock import patch


def test_summarize_endpoint(client):
    with patch(
        "app.api.endpoints.summarize.summarize",
        return_value={"summary": "Mock summary", "provider": "mock"},
    ):
        response = client.post(
            "/summarize/",
            json={"text": "FastAPI is a modern Python framework for building APIs."},
        )
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["summary"] == "Mock summary"
        assert json_data["provider"] == "mock"


def test_summarize_invalid_length(client):
    response = client.post(
        "/summarize/", json={"text": "This is test text.", "length": "gigantic"}
    )
    assert response.status_code == 422
    json_data = response.json()
    assert "detail" in json_data


def test_summarize_missing_text(client):
    response = client.post("/summarize/", json={"length": "short"})
    assert response.status_code == 422
