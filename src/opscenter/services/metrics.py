from datetime import date, timedelta
from typing import Any

from opscenter.database import db


def get_dashboard_metrics() -> dict[str, Any]:
    today = date.today()
    seven_days = today + timedelta(days=7)
    inactive_cutoff = today - timedelta(days=14)

    with db.connect() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_projects,
                SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_projects,
                SUM(CASE WHEN date(last_updated) < date(?) AND status != 'Complete' THEN 1 ELSE 0 END)
                    AS inactive_projects
            FROM projects
            """,
            (inactive_cutoff.isoformat(),),
        ).fetchone()

        task_row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_tasks,
                SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_tasks,
                SUM(CASE WHEN due_date IS NOT NULL
                    AND due_date != ''
                    AND date(due_date) < date(?)
                    AND status != 'Complete' THEN 1 ELSE 0 END) AS overdue_tasks,
                SUM(CASE WHEN due_date IS NOT NULL
                    AND due_date != ''
                    AND date(due_date) BETWEEN date(?) AND date(?)
                    AND status != 'Complete' THEN 1 ELSE 0 END) AS due_soon_tasks
            FROM tasks
            """,
            (today.isoformat(), today.isoformat(), seven_days.isoformat()),
        ).fetchone()

        due_soon = connection.execute(
            """
            SELECT
                tasks.name,
                tasks.due_date,
                tasks.priority,
                tasks.status,
                COALESCE(projects.name, 'No project') AS project_name
            FROM tasks
            LEFT JOIN projects ON projects.id = tasks.project_id
            WHERE tasks.due_date IS NOT NULL
                AND tasks.due_date != ''
                AND date(tasks.due_date) BETWEEN date(?) AND date(?)
                AND tasks.status != 'Complete'
            ORDER BY date(tasks.due_date), tasks.priority DESC
            LIMIT 20
            """,
            (today.isoformat(), seven_days.isoformat()),
        ).fetchall()

        overdue = connection.execute(
            """
            SELECT
                tasks.name,
                tasks.due_date,
                tasks.priority,
                tasks.status,
                COALESCE(projects.name, 'No project') AS project_name
            FROM tasks
            LEFT JOIN projects ON projects.id = tasks.project_id
            WHERE tasks.due_date IS NOT NULL
                AND tasks.due_date != ''
                AND date(tasks.due_date) < date(?)
                AND tasks.status != 'Complete'
            ORDER BY date(tasks.due_date), tasks.priority DESC
            LIMIT 20
            """,
            (today.isoformat(),),
        ).fetchall()

        inactive_projects = connection.execute(
            """
            SELECT name, status, priority, last_updated
            FROM projects
            WHERE date(last_updated) < date(?)
                AND status != 'Complete'
            ORDER BY date(last_updated), priority DESC
            LIMIT 20
            """,
            (inactive_cutoff.isoformat(),),
        ).fetchall()

    return {
        "total_projects": row["total_projects"] or 0,
        "active_projects": row["active_projects"] or 0,
        "inactive_projects": row["inactive_projects"] or 0,
        "total_tasks": task_row["total_tasks"] or 0,
        "active_tasks": task_row["active_tasks"] or 0,
        "overdue_tasks": task_row["overdue_tasks"] or 0,
        "due_soon_tasks": task_row["due_soon_tasks"] or 0,
        "due_soon_table": due_soon,
        "overdue_table": overdue,
        "inactive_projects_table": inactive_projects,
    }
