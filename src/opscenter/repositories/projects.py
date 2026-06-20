from datetime import date
from typing import Any

from opscenter.database import db


def list_projects(
    search: str = "",
    status: str = "All",
    priority: str = "All",
) -> list[dict[str, Any]]:
    clauses: list[str] = []
    params: list[Any] = []

    if search:
        clauses.append("(LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(description) LIKE ?)")
        search_term = f"%{search.lower()}%"
        params.extend([search_term, search_term, search_term])
    if status != "All":
        clauses.append("status = ?")
        params.append(status)
    if priority != "All":
        clauses.append("priority = ?")
        params.append(priority)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"""
        SELECT id, name, category, description, priority, status, date_created, last_updated
        FROM projects
        {where}
        ORDER BY
            CASE priority
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                ELSE 4
            END,
            last_updated DESC,
            name COLLATE NOCASE
    """
    with db.connect() as connection:
        return connection.execute(query, params).fetchall()


def get_project(project_id: int) -> dict[str, Any] | None:
    with db.connect() as connection:
        return connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()


def create_project(values: dict[str, Any]) -> None:
    today = date.today().isoformat()
    with db.connect() as connection:
        connection.execute(
            """
            INSERT INTO projects
                (name, category, description, priority, status, date_created, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                values["name"],
                values["category"],
                values["description"],
                values["priority"],
                values["status"],
                today,
                values.get("last_updated") or today,
            ),
        )


def update_project(project_id: int, values: dict[str, Any]) -> None:
    with db.connect() as connection:
        connection.execute(
            """
            UPDATE projects
            SET name = ?,
                category = ?,
                description = ?,
                priority = ?,
                status = ?,
                last_updated = ?
            WHERE id = ?
            """,
            (
                values["name"],
                values["category"],
                values["description"],
                values["priority"],
                values["status"],
                values["last_updated"],
                project_id,
            ),
        )


def delete_project(project_id: int) -> None:
    with db.connect() as connection:
        connection.execute("DELETE FROM projects WHERE id = ?", (project_id,))
