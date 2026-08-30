import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_ping_get():
    response = client.get("/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["ping"] == "pong"
    assert "timestamp" in data


def test_root_ping_head():
    response = client.head("/ping")
    assert response.status_code == 200


def test_root_health_get():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "uptime_seconds" in data
    assert data["database"] == "healthy"
    assert data["database_connected"] is True
    assert "pytorch_version" in data
    assert "pennylane_version" in data
    assert "timestamp" in data


def test_root_health_head():
    response = client.head("/health")
    assert response.status_code == 200


def test_root_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_root_livez():
    response = client.get("/livez")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


def test_root_readyz():
    response = client.get("/readyz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "healthy"


def test_api_prefixed_health_and_ping():
    resp_health = client.get("/api/health")
    assert resp_health.status_code == 200
    assert resp_health.json()["status"] == "online"

    resp_ping = client.get("/api/ping")
    assert resp_ping.status_code == 200
    assert resp_ping.json()["ping"] == "pong"
