def test_root_returns_404(client):
    response = client.get("/")
    assert response.status_code == 404
    assert "Not found" in response.text
