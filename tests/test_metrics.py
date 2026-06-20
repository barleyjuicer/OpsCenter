from datetime import date, timedelta
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import opscenter.services.metrics as metrics
from opscenter.database import Database


class MetricsTests(unittest.TestCase):
    def test_dashboard_metrics_use_temporary_database(self):
        with TemporaryDirectory() as temp_dir:
            database = Database(Path(temp_dir) / "metrics_test.db")
            database.initialize()
            original_db = metrics.db
            metrics.db = database

            try:
                today = date.today()
                with database.connect() as connection:
                    connection.execute(
                        """
                        INSERT INTO projects
                            (name, category, description, priority, status, date_created, last_updated)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            "Sample Project",
                            "Operations",
                            "Fake test project",
                            "High",
                            "Active",
                            today.isoformat(),
                            (today - timedelta(days=20)).isoformat(),
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO tasks
                            (project_id, name, description, due_date, priority, status, date_created, last_updated)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            1,
                            "Sample Task",
                            "Fake test task",
                            (today - timedelta(days=1)).isoformat(),
                            "Critical",
                            "Active",
                            today.isoformat(),
                            today.isoformat(),
                        ),
                    )

                result = metrics.get_dashboard_metrics()
            finally:
                metrics.db = original_db

        self.assertEqual(result["total_projects"], 1)
        self.assertEqual(result["active_projects"], 1)
        self.assertEqual(result["inactive_projects"], 1)
        self.assertEqual(result["total_tasks"], 1)
        self.assertEqual(result["active_tasks"], 1)
        self.assertEqual(result["overdue_tasks"], 1)


if __name__ == "__main__":
    unittest.main()
