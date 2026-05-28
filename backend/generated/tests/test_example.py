import pytest
from fastapi.testclient import TestClient

# Import the generated modules
from generated.code.services.task_service import TaskService
from generated.code.routes.tasks import router

# Create a FastAPI app for testing
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)

# ---------- Service Layer Tests ----------


def test_create_task_success():
    service = TaskService()
    task = service.create_task("Buy milk")
    assert task.title == "Buy milk"
    assert task.completed is False
    assert isinstance(task.id, str)
    assert len(service.list_tasks()) == 1


def test_create_task_empty_title_raises():
    service = TaskService()
    with pytest.raises(ValueError) as exc:
        service.create_task("")
    assert "required" in str(exc.value)


def test_create_task_title_exceeds_max_length_raises():
    service = TaskService()
    long_title = "a" * 101
    with pytest.raises(ValueError) as exc:
        service.create_task(long_title)
    assert "cannot exceed" in str(exc.value)


# ---------- API Endpoint Tests ----------


def test_post_task_success():
    response = client.post("/tasks", json={"title": "Read book"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read book"
    assert data["completed"] is False
    assert "id" in data


def test_post_task_empty_title_returns_400():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 400
    assert "required" in response.json()["detail"]


def test_post_task_title_exceeds_max_length_returns_400():
    response = client.post("/tasks", json={"title": "a" * 101})
    assert response.status_code == 400
    assert "cannot exceed" in response.json()["detail"]


def test_get_tasks_returns_all_created_tasks():
    # Create two tasks via the API
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 2
    titles = {t["title"] for t in tasks}
    assert "Task 1" in titles
    assert "Task 2" in titles
