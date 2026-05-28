from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.task_service import TaskService

router = APIRouter()
task_service = TaskService()


class TaskCreate(BaseModel):
    title: str


@router.post("/tasks")
async def create_task(payload: TaskCreate):
    try:
        task = task_service.create_task(payload.title)
        return {"id": task.id, "title": task.title, "completed": task.completed}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks")
async def get_tasks():
    tasks = task_service.list_tasks()
    return [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
