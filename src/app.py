from datetime import date
from typing import Any

import streamlit as st

from opscenter.config import (
    APP_NAME,
    PROJECT_CATEGORIES,
    PROJECT_PRIORITIES,
    STATUSES,
    TASK_PRIORITIES,
)
from opscenter.database import db
from opscenter.repositories import projects as project_repo
from opscenter.repositories import tasks as task_repo
from opscenter.services.metrics import get_dashboard_metrics
from opscenter.ui import apply_style, display_table, metric_card, page_header


st.set_page_config(page_title=APP_NAME, page_icon=":material/dashboard:", layout="wide")
db.initialize()
apply_style()


def rerun() -> None:
    st.rerun()


def project_options() -> dict[str, int | None]:
    records = project_repo.list_projects()
    options: dict[str, int | None] = {"No project": None}
    options.update({record["name"]: record["id"] for record in records})
    return options


def status_index(value: str) -> int:
    return STATUSES.index(value) if value in STATUSES else 0


def priority_index(value: str) -> int:
    return PROJECT_PRIORITIES.index(value) if value in PROJECT_PRIORITIES else 1


def parse_date(value: str | None) -> date:
    if not value:
        return date.today()
    return date.fromisoformat(value)


def dashboard_page() -> None:
    page_header("Dashboard", "Your project and task command center.")
    metrics = get_dashboard_metrics()

    row_one = st.columns(5)
    with row_one[0]:
        metric_card("Total Projects", metrics["total_projects"], "All tracked projects")
    with row_one[1]:
        metric_card("Active Projects", metrics["active_projects"], "Currently moving")
    with row_one[2]:
        metric_card("Due In 7 Days", metrics["due_soon_tasks"], "Open tasks")
    with row_one[3]:
        metric_card("Overdue Tasks", metrics["overdue_tasks"], "Needs attention")
    with row_one[4]:
        metric_card("Inactive Projects", metrics["inactive_projects"], "No update in 14 days")

    row_two = st.columns(2)
    with row_two[0]:
        metric_card("Total Tasks", metrics["total_tasks"], "All tracked tasks")
    with row_two[1]:
        metric_card("Active Tasks", metrics["active_tasks"], "In progress now")

    st.markdown('<div class="section-title">Tasks Due In The Next 7 Days</div>', unsafe_allow_html=True)
    display_table(metrics["due_soon_table"], "No tasks are due in the next 7 days.")

    st.markdown('<div class="section-title">Overdue Tasks</div>', unsafe_allow_html=True)
    display_table(metrics["overdue_table"], "No overdue tasks.")

    st.markdown('<div class="section-title">Projects Not Updated In 14 Days</div>', unsafe_allow_html=True)
    display_table(metrics["inactive_projects_table"], "No inactive projects.")


def project_form(existing: dict[str, Any] | None = None) -> dict[str, Any] | None:
    existing = existing or {}
    category_value = existing.get("category", "General")
    category_index = PROJECT_CATEGORIES.index(category_value) if category_value in PROJECT_CATEGORIES else 0

    name = st.text_input("Project Name", value=existing.get("name", ""))
    category = st.selectbox("Category", PROJECT_CATEGORIES, index=category_index)
    description = st.text_area("Description", value=existing.get("description", ""), height=110)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        priority = st.selectbox("Priority", PROJECT_PRIORITIES, index=priority_index(existing.get("priority", "Medium")))
    with col_b:
        status = st.selectbox("Status", STATUSES, index=status_index(existing.get("status", "Backlog")))
    with col_c:
        last_updated = st.date_input("Last Updated", value=parse_date(existing.get("last_updated")))

    return {
        "name": name.strip(),
        "category": category,
        "description": description.strip(),
        "priority": priority,
        "status": status,
        "last_updated": last_updated.isoformat(),
    }


def projects_page() -> None:
    page_header("Projects", "Plan, prioritize, and maintain the work that matters.")

    with st.expander("Add Project", expanded=False):
        with st.form("add_project"):
            values = project_form()
            submitted = st.form_submit_button("Add Project", type="primary")
            if submitted and values and values["name"]:
                project_repo.create_project(values)
                st.success("Project added.")
                rerun()
            elif submitted:
                st.warning("Project name is required.")

    st.subheader("Search And Filter")
    filter_cols = st.columns([2, 1, 1])
    search = filter_cols[0].text_input("Search projects", placeholder="Name, category, or description")
    status = filter_cols[1].selectbox("Status", ["All"] + STATUSES)
    priority = filter_cols[2].selectbox("Priority", ["All"] + PROJECT_PRIORITIES)

    records = project_repo.list_projects(search=search, status=status, priority=priority)
    display_records = [
        {
            "Project Name": row["name"],
            "Category": row["category"],
            "Priority": row["priority"],
            "Status": row["status"],
            "Date Created": row["date_created"],
            "Last Updated": row["last_updated"],
            "Description": row["description"],
        }
        for row in records
    ]
    display_table(display_records, "No projects match the current filters.")

    st.subheader("Edit Or Delete Project")
    if not records:
        st.caption("Add a project to enable editing.")
        return

    selected_label = st.selectbox("Choose project", [f"{row['name']} #{row['id']}" for row in records])
    selected_id = int(selected_label.rsplit("#", 1)[1])
    selected = project_repo.get_project(selected_id)

    edit_col, delete_col = st.columns([2, 1])
    with edit_col:
        with st.form("edit_project"):
            values = project_form(selected)
            submitted = st.form_submit_button("Save Changes", type="primary")
            if submitted and values and values["name"]:
                project_repo.update_project(selected_id, values)
                st.success("Project updated.")
                rerun()
            elif submitted:
                st.warning("Project name is required.")

    with delete_col:
        st.write("Delete")
        st.caption("Deletion removes the project. Related tasks are kept and marked as No project.")
        confirm = st.checkbox("I understand this cannot be undone", key=f"confirm_project_{selected_id}")
        if st.button("Delete Project", disabled=not confirm, type="secondary"):
            project_repo.delete_project(selected_id)
            st.success("Project deleted.")
            rerun()


def task_form(existing: dict[str, Any] | None = None) -> dict[str, Any] | None:
    existing = existing or {}
    options = project_options()
    labels = list(options.keys())
    current_project_id = existing.get("project_id")
    current_label = next((label for label, project_id in options.items() if project_id == current_project_id), "No project")

    name = st.text_input("Task Name", value=existing.get("name", ""))
    project_label = st.selectbox("Parent Project", labels, index=labels.index(current_label))
    description = st.text_area("Description", value=existing.get("description", ""), height=110)

    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        due_date = st.date_input("Due Date", value=parse_date(existing.get("due_date")))
    with col_b:
        priority = st.selectbox("Priority", TASK_PRIORITIES, index=priority_index(existing.get("priority", "Medium")))
    with col_c:
        status = st.selectbox("Status", STATUSES, index=status_index(existing.get("status", "Backlog")))
    with col_d:
        last_updated = st.date_input("Last Updated", value=parse_date(existing.get("last_updated")), key=f"task_updated_{existing.get('id', 'new')}")

    no_due_date = st.checkbox("No due date", value=not bool(existing.get("due_date")))

    return {
        "project_id": options[project_label],
        "name": name.strip(),
        "description": description.strip(),
        "due_date": None if no_due_date else due_date.isoformat(),
        "priority": priority,
        "status": status,
        "last_updated": last_updated.isoformat(),
    }


def tasks_page() -> None:
    page_header("Tasks", "Capture commitments and keep execution visible.")

    with st.expander("Add Task", expanded=False):
        with st.form("add_task"):
            values = task_form()
            submitted = st.form_submit_button("Add Task", type="primary")
            if submitted and values and values["name"]:
                task_repo.create_task(values)
                st.success("Task added.")
                rerun()
            elif submitted:
                st.warning("Task name is required.")

    st.subheader("Filter Tasks")
    options = project_options()
    filter_cols = st.columns(3)
    project_label = filter_cols[0].selectbox("Project", ["All"] + list(options.keys()))
    status = filter_cols[1].selectbox("Status", ["All"] + STATUSES)
    priority = filter_cols[2].selectbox("Priority", ["All"] + TASK_PRIORITIES)
    filtered_project_id = None if project_label == "All" else options[project_label]

    records = task_repo.list_tasks(project_id=filtered_project_id, status=status, priority=priority)
    display_records = [
        {
            "Task Name": row["name"],
            "Parent Project": row["project_name"],
            "Due Date": row["due_date"] or "",
            "Priority": row["priority"],
            "Status": row["status"],
            "Date Created": row["date_created"],
            "Last Updated": row["last_updated"],
            "Description": row["description"],
        }
        for row in records
    ]
    display_table(display_records, "No tasks match the current filters.")

    st.subheader("Edit Or Delete Task")
    if not records:
        st.caption("Add a task to enable editing.")
        return

    selected_label = st.selectbox("Choose task", [f"{row['name']} #{row['id']}" for row in records])
    selected_id = int(selected_label.rsplit("#", 1)[1])
    selected = task_repo.get_task(selected_id)

    edit_col, delete_col = st.columns([2, 1])
    with edit_col:
        with st.form("edit_task"):
            values = task_form(selected)
            submitted = st.form_submit_button("Save Changes", type="primary")
            if submitted and values and values["name"]:
                task_repo.update_task(selected_id, values)
                st.success("Task updated.")
                rerun()
            elif submitted:
                st.warning("Task name is required.")

    with delete_col:
        st.write("Delete")
        st.caption("Deletion removes the selected task permanently.")
        confirm = st.checkbox("I understand this cannot be undone", key=f"confirm_task_{selected_id}")
        if st.button("Delete Task", disabled=not confirm, type="secondary"):
            task_repo.delete_task(selected_id)
            st.success("Task deleted.")
            rerun()


def main() -> None:
    st.sidebar.title(APP_NAME)
    page = st.sidebar.radio("Navigate", ["Dashboard", "Projects", "Tasks"], label_visibility="collapsed")
    st.sidebar.divider()
    st.sidebar.caption("Local SQLite storage. No cloud dependencies.")

    if page == "Dashboard":
        dashboard_page()
    elif page == "Projects":
        projects_page()
    else:
        tasks_page()


if __name__ == "__main__":
    main()
