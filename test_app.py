import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app import app  # noqa: E402


def test_health():
    client = app.test_client()
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_create_and_list_task():
    client = app.test_client()
    resp = client.post("/api/tasks", json={"title": "Write workshop docs"})
    assert resp.status_code == 201

    resp = client.get("/api/tasks")
    assert resp.status_code == 200
    titles = [t["title"] for t in resp.get_json()]
    assert "Write workshop docs" in titles
