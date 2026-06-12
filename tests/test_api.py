from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["timestamp"], int)
    assert body["uptime_seconds"] >= 0


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    body = response.json()
    assert "cpu_percent" in body
    assert 0 <= body["memory"]["percent"] <= 100
    assert 0 <= body["disk"]["percent"] <= 100


def test_info_endpoint() -> None:
    response = client.get("/info")

    assert response.status_code == 200
    body = response.json()
    assert body["hostname"]
    assert body["system"]
    assert body["python_version"]
