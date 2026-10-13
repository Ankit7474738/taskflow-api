from fastapi import FastAPI
from app.routes import router as tasks_router

app = FastAPI(
    title="TaskFlow API",
    description="A small task-management API for repository-agent testing.",
    version="1.0.0",
)
app.include_router(tasks_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
