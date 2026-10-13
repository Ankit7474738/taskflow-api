import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repository import repository

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    repository.clear()
    yield
    repository.clear()


def create_task(title: str, status: str = "todo", priority: str = "medium") -> dict:
    response = client.post("/tasks", json={
        "title": title, "status": status, "priority": priority
    })
    assert response.status_code == 201
    return response.json()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_task():
    created = create_task("Write tests")
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Write tests"


def test_list_tasks_can_filter_by_status():
    create_task("First", status="todo")
    create_task("Second", status="done")
    response = client.get("/tasks?status=done")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert [x["title"] for x in response.json()["items"]] == ["Second"]


def test_list_tasks_can_filter_by_priority():
    create_task("Low", priority="low")
    create_task("High", priority="high")
    response = client.get("/tasks?priority=high")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["title"] == "High"


def test_pagination_total_is_counted_after_filtering():
    create_task("One", status="todo")
    create_task("Two", status="todo")
    create_task("Three", status="done")
    response = client.get("/tasks?status=todo&page=2&page_size=1")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 1
    assert body["page"] == 2


def test_update_task():
    created = create_task("Original")
    response = client.patch(f"/tasks/{created['id']}", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_delete_task():
    created = create_task("Temporary")
    assert client.delete(f"/tasks/{created['id']}").status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_invalid_status_is_rejected():
    assert client.get("/tasks?status=unknown").status_code == 422


def test_empty_title_is_rejected():
    assert client.post("/tasks", json={"title": ""}).status_code == 422
