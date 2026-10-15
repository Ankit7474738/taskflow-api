def filter_tasks(..., overdue_only: Optional[bool] = None, ...):
    if overdue_only:
        tasks = [task for task in tasks if task.due_date and task.due_date < datetime.now() and task.status != 'done']
    return tasks