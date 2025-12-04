from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_eta_route():
    res = client.get("/shipping/eta?vessel_class=QFlex")
    assert res.status_code == 200
    body = res.json()

    assert "eta" in body
    assert "origin" in body
