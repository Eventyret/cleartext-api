import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import verify_internal_api_key


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[verify_internal_api_key] = lambda: None
    yield TestClient(app)
    app.dependency_overrides = {}
