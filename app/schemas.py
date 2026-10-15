class TaskCreate(BaseModel):
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    due_date: Optional[datetime] = None