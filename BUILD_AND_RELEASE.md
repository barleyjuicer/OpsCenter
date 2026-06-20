# Build And Release

## Local Development

1. Install Python 3.10 or newer.
2. Create a virtual environment in `.venv`.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Run the app with `python -m streamlit run src/app.py`.

The application creates `data/opscenter.db` automatically. That database is private local data and must not be committed.

## Testing

Run:

```powershell
python -m unittest discover -s tests
```

Tests must use temporary databases or fake data from `sample_data/`. Tests must never require real PHI, PII, personal records, private reports, or private exports.

## Release Packaging

Run:

```powershell
packaging\package_for_sharing.bat
```

The release ZIP is created next to the project folder. The packaging script excludes:

- local databases and private data
- reports and exports
- virtual environments
- caches and build artifacts
- logs and screenshots

Before sharing, inspect the ZIP contents and confirm no private records are included.

## Owner-Directed AI Assistance

This repository may be developed with AI assistance. The repository owner directs the work, reviews generated changes, and is responsible for confirming correctness, privacy, and release readiness.
