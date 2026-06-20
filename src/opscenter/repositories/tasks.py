from datetime import date
from typing import Any

from opscenter.database import db


def list_tasks(
    project_id: int | None = None,
    status: str = "All",
    priority: str = "All",
) -> list[dict[str, Any]]:
    clauses: list[str] = []
    params: list[Any] = []

    if project_id:
        clauses.append("tasks.project_id = ?")
        params.append(project_id)
    if status != "All":
        clauses.append("tasks.status = ?")
        params.append(status)
    if priority != "All":
        clauses.append("tasks.priority = ?")
        params.append(priority)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"""
        SELECT
            tasks.id,
            tasks.name,
            tasks.description,
            tasks.due_date,
            tasks.priority,
            tasks.status,
            tasks.date_created,
            tasks.last_updated,
            tasks.project_id,
            COALESCE(projects.name, 'No project') AS project_name
        FROM tasks
        LEFT JOIN projects ON projects.id = tasks.project_id
        {where}
        ORDER BY
            CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END,
            due_date ASC,
            CASE tasks.priority
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                ELSE 4
            END,
            tasks.name COLLATE NOCASE
    """
    with db.connect() as connection:
        return connection.execute(query, params).fetchall()


def get_task(task_id: int) -> dict[str, Any] | None:
    with db.connect() as connection:
        return connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()


def create_task(values: dict[str, Any]) -> None:
    today = date.today().isoformat()
    with db.connect() as connection:
        connection.execute(
            """
            INSERT INTO tasks
                (project_id, name, description, due_date, priority, status, date_created, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                values["project_id"],
                values["name"],
                values["description"],
                values["due_date"],
                values["priority"],
                values["status"],
                today,
                values.get("last_updated") or today,
            ),
        )


def update_task(task_id: int, values: dict[str, Any]) -> None:
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE tasks
            SET project_id = ?,
                name = ?,
                description = ?,
                due_date = ?,
                priority = ?,
                status = ?,
                last_updated = ?
            WHERE id = ?
            """,
            (
                values["project_id"],
                values["name"],
                values["description"],
                values["due_date"],
                values["priority"],
                values["status"],
                values["last_updated"],
                task_id,
            ),
        )


def delete_task(task_id: int) -> None:
    with db.connect() as connection:
        connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
