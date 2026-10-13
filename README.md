# TaskFlow API

A compact Python/FastAPI task-management API designed for testing repository-analysis agents.

## Features
- Create, list, retrieve, update, and delete tasks
- Filter by status and priority
- Pagination with total count
- In-memory storage (data resets on restart)

## Run
Python 3.10+ required.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Tests
```powershell
pytest -q
```

## Example
```powershell
curl "http://127.0.0.1:8000/tasks?status=todo&priority=high&page=1&page_size=10"
```

## Structure
- `app/models.py`: task domain model and enums
- `app/schemas.py`: request/response validation
- `app/repository.py`: in-memory persistence
- `app/services.py`: business logic and filtering
- `app/routes.py`: HTTP endpoints
- `tests/test_tasks.py`: API tests

This is a demo, not a production service. It has no authentication or persistent database.
