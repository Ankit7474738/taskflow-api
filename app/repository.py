from app.models import Task


class TaskRepository:
    # Simple in-memory persistence for this demo.
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def list(self) -> list[Task]:
        return list(self._tasks.values())

    def delete(self, task_id: str) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def clear(self) -> None:
        self._tasks.clear()


repository = TaskRepository()
