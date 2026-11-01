from fastapi import APIRouter, HTTPException, Query, Response, status
from app.models import TaskPriority, TaskStatus
from app.repository import repository
from app.schemas import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.services import TaskNotFoundError, TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])
task_service = TaskService(repository)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskResponse:
    return task_service.create(payload)


@router.get("", response_model=TaskListResponse)
def list_tasks(
    status_filter: TaskStatus | None = Query(default=None, alias="status"),
    priority: TaskPriority | None = None,
    overdue_only: bool = False,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> TaskListResponse:
    items, total = task_service.list_tasks(
        status=status_filter,
        priority=priority,
        overdue_only=overdue_only,
        page=page,
        page_size=page_size,
    )
    return TaskListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str) -> TaskResponse:
    try:
        return task_service.get(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    try:
        return task_service.update(task_id, payload)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> Response:
    try:
        task_service.delete(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
