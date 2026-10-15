def test_get_tasks_overdue(...):
    response = client.get('/tasks', params={'overdue_only': True})
    assert response.status_code == 200
    tasks = response.json()
    assert all(task['due_date'] and task['due_date'] < datetime.now() and task['status'] != 'done' for task in tasks)