from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_whoami():
    response = client.get("/whoami")

    assert response.status_code == 200
    assert "hostname" in response.json()