import uuid


class Task:
    def __init__(self, title: str, task_id: str = None, completed: bool = False):
        self.id = task_id if task_id is not None else str(uuid.uuid4())
        self.title = title
        self.completed = completed
