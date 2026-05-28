from ..models.task import Task


class TaskService:
    def __init__(self):
        self.tasks: list[Task] = []

    def create_task(self, title: str) -> Task:
        if not title or title.strip() == "":
            raise ValueError("Task title is required")
        if len(title) > 100:
            raise ValueError("Task title cannot exceed 100 characters")
        task = Task(title=title.strip())
        self.tasks.append(task)
        return task

    def list_tasks(self) -> list[Task]:
        return self.tasks.copy()
