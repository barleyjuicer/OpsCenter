import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opscenter.database import Database


class DatabaseTests(unittest.TestCase):
    def test_database_initializes_schema(self):
        with TemporaryDirectory() as temp_dir:
            database = Database(Path(temp_dir) / "opscenter_test.db")
            database.initialize()

            with database.connect() as connection:
                tables = {
                    row["name"]
                    for row in connection.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    ).fetchall()
                }

        self.assertIn("projects", tables)
        self.assertIn("tasks", tables)
        self.assertIn("schema_migrations", tables)


if __name__ == "__main__":
    unittest.main()
