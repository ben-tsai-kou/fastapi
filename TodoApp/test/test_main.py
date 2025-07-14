from fastapi.testclient import TestClient
from fastapi import status
import pytest


@pytest.fixture
def client():
    from main import app

    return TestClient(app)


def test_return_health_check(client):
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
