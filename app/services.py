from app.models import Task
from app.repository import TaskRepository
from app.schemas import TaskCreate, TaskUpdate
from app.models import TaskPriority, TaskStatus
from datetime import datetime, timezone


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def create(self, data: TaskCreate) -> Task:
            task = Task(
                title=data.title.strip(),
                description=data.description,
                status=data.status,
                priority=data.priority,
            )
            if data.due_date is not None:
                task.due_date = data.due_date
            return self.repository.add(task)

    def get(self, task_id: str) -> Task:
        task = self.repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def list_tasks(
            self,
            status: TaskStatus | None = None,
            priority: TaskPriority | None = None,
            overdue_only: bool = False,
            page: int = 1,
            page_size: int = 20,
        ) -> tuple[list[Task], int]:
            tasks = self.repository.list()
            if status is not None:
                tasks = [task for task in tasks if task.status == status]
            if priority is not None:
                tasks = [task for task in tasks if task.priority == priority]
            if overdue_only:
                now = datetime.now(timezone.utc)
                tasks = [
                    task
                    for task in tasks
                    if getattr(task, "due_date", None) is not None
                    and task.due_date < now
                    and task.status != TaskStatus.DONE
                ]
            tasks.sort(key=lambda task: task.created_at, reverse=True)
            total = len(tasks)
            start = (page - 1) * page_size
            return tasks[start:start + page_size], total

    def update(self, task_id: str, data: TaskUpdate) -> Task:
        task = self.get(task_id)
        for field_name, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                if field_name == "title":
                    value = value.strip()
                setattr(task, field_name, value)
        task.touch()
        return task

    def delete(self, task_id: str) -> None:
        if not self.repository.delete(task_id):
            raise TaskNotFoundError(task_id)
