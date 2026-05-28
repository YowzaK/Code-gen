import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from generated.code.routes.tasks import router as task_router


@pytest.fixture(scope="function")
def client():
    app = FastAPI()
    app.include_router(task_router)
    return TestClient(app)


def test_create_task_success(client):
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["completed"] is False
    assert isinstance(data["id"], int)


def test_create_task_empty_title(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422  # validation error from FastAPI/Pydantic
    # Ensure error mentions title
    assert "title" in response.text.lower()


def test_create_task_over_limit_title(client):
    long_title = "a" * 101
    response = client.post("/tasks", json={"title": long_title})
    assert response.status_code == 422
    assert "title" in response.text.lower()


def test_list_tasks_returns_created_tasks(client):
    # Create two tasks
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    # Retrieve list
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    titles = [task["title"] for task in data]
    assert "Task 1" in titles
    assert "Task 2" in titles
    # Ensure each task has required fields
    for task in data:
        assert isinstance(task["id"], int)
        assert isinstance(task["title"], str)
        assert isinstance(task["completed"], bool)
