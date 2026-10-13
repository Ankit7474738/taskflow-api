# GitHub issue: Add due-date support and overdue filtering for tasks

**Labels:** enhancement, good first issue (optional)

## Summary
Add an optional due date to tasks and allow clients to filter the task list to overdue tasks.

## Motivation
The API currently filters by status and priority, but it cannot represent deadlines or quickly find tasks whose deadlines have passed.

## Requirements
1. Add an optional `due_date` field to task creation, update, and response schemas. Accept ISO-8601 dates or datetimes; choose one representation, document it, and use it consistently.
2. Store the due date on the domain `Task` model. Existing requests without `due_date` must continue to work.
3. Add an `overdue_only` boolean query parameter to `GET /tasks`.
4. When `overdue_only=true`, return tasks whose due date is earlier than the current time and whose status is not `done`.
5. Tasks without a due date must not be considered overdue.
6. Compose this filter with existing `status`, `priority`, `page`, and `page_size` filters. `total` must count matching tasks after all filters but before pagination.
7. Add tests for past-due, future-due, completed past-due, no due date, invalid input, and combined filters.
8. Add a README example request.

## Acceptance criteria
- Existing tests continue to pass.
- New tests pass with `pytest -q`.
- Invalid due-date input returns HTTP 422.
- `GET /tasks?overdue_only=true` excludes completed and undated tasks.
- Filtering and pagination remain correct.

## Scope
Do not add a database, authentication, background scheduler, or external date/time service. Keep the change consistent with the current architecture.
