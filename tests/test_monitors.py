import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models import Monitor, CheckResult


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client
    SQLModel.metadata.drop_all(engine)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_monitor(client):
    response = client.post("/monitors/", json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()

    assert data["id"] is not None
    assert data["url"] == "https://example.com"


def test_get_monitors(client):
    client.post("/monitors/", json={"url": "https://example.com"})

    response = client.get("/monitors/")

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["url"] == "https://example.com"


def test_get_history_empty(client):
    response = client.post("/monitors/", json={"url": "https://example.com"})
    monitor_id = response.json()["id"]

    response = client.get(f"/monitors/{monitor_id}/history")

    assert response.status_code == 200
    assert response.json() == []


def test_get_history_not_found(client):
    response = client.get("/monitors/999/history")

    assert response.status_code == 404


def test_delete_monitor(client):
    response = client.post("/monitors/", json={"url": "https://example.com"})
    monitor_id = response.json()["id"]

    response = client.delete(f"/monitors/{monitor_id}")

    assert response.status_code == 200

    # confirm deletion
    response = client.get("/monitors/")
    assert len(response.json()) == 0


def test_delete_monitor_not_found(client):
    response = client.delete("/monitors/999")

    assert response.status_code == 404