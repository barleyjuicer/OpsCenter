from pathlib import Path


APP_NAME = "OpsCenter"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "opscenter.db"

PROJECT_PRIORITIES = ["Low", "Medium", "High", "Critical"]
TASK_PRIORITIES = PROJECT_PRIORITIES
STATUSES = ["Backlog", "Active", "Waiting", "Complete"]
PROJECT_CATEGORIES = [
    "General",
    "Operations",
    "Knowledge",
    "Job Tracking",
    "Study",
    "Health",
    "Finance",
]
