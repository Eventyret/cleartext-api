from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)


def test_title_generates_successfully():
    with patch(
        "app.api.endpoints.title.generate_title", return_value="Mocked Title"
    ) as mock_gen:
        response = client.post("/title/", json={"text": "This is a test passage"})
        assert response.status_code == 200
        assert response.json() == {"title": "Mocked Title"}
        mock_gen.assert_called_once()


def test_title_rejects_empty_input_early():
    mock = Mock()
    with patch("app.api.endpoints.title.generate_title", new=mock):
        response = client.post("/title/", json={"text": ""})
        assert response.status_code == 422
        mock.assert_not_called()


def test_title_fails_when_providers_exhausted():
    with patch(
        "app.api.endpoints.title.generate_title",
        side_effect=Exception("All providers failed"),
    ):
        response = client.post("/title/", json={"text": "This should fail"})
        assert response.status_code == 500
        assert (
            response.json()["detail"] == "Internal server error during title generation"
        )
