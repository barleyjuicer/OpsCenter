# OpsCenter

OpsCenter is a local desktop-style operations dashboard for projects, tasks, and executive metrics. It runs with Python, Streamlit, and SQLite. Your private data stays on your computer in `data/opscenter.db`.

## Install And Run

1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. Open the repository folder.
3. Double-click `packaging\install_and_run.bat`.
4. A browser window opens with the app.

The installer creates a local `.venv` folder, installs requirements, and starts `src/app.py`.

## Privacy And GitHub Safety

Never commit real user databases, reports, exports, logs, screenshots, or any PHI/PII. Real local records belong only in:

- `data/` for SQLite databases and local working data.
- `exports/` for CSV, XLSX, PDF, and other exported files.
- `reports/` for generated reports.

Those folders contain placeholder files so the directories appear in GitHub, but their real contents are ignored by `.gitignore`.

Fake examples may be committed only under `sample_data/`.

## Share The App

Run `packaging\package_for_sharing.bat` to create a clean source ZIP next to the project folder.

The ZIP includes source files, docs, tests, and install scripts. It excludes local databases, private exports, reports, virtual environments, logs, screenshots, and generated caches.

## Project Structure

- `src/app.py` - Streamlit user interface.
- `src/opscenter/database.py` - SQLite connection, migrations, and future schema expansion point.
- `src/opscenter/repositories/` - Data access layer for projects and tasks.
- `src/opscenter/services/metrics.py` - Dashboard metric calculations.
- `src/opscenter/ui.py` - Shared styling and display helpers.
- `data/opscenter.db` - Local SQLite database created automatically on first run and ignored by Git.
- `docs/` - Repository guidance and data safety notes.
- `packaging/` - Release and sharing utilities.
- `tests/` - Tests that run without real private data.

## Development Approach

This is an AI-assisted project directed by the repository owner. AI tools may help draft code, documentation, tests, and refactors, but the owner decides project goals, reviews changes, and controls what is released or committed.

## Notes

- No cloud services are used.
- Tables are created automatically if missing.
- Source code and tests do not require real PHI/PII to run.
- The schema includes a migration table so future modules can be added safely.
