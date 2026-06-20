# GitHub Data Safety

OpsCenter is designed so source code can be shared without sharing private user data.

## Commit

- application source in `src/`
- tests in `tests/`
- documentation in `docs/`
- fake examples in `sample_data/`
- placeholder files such as `.gitkeep`

## Do Not Commit

- real SQLite databases
- PHI, PII, or personal records
- generated reports
- CSV, XLSX, or PDF exports
- logs
- screenshots
- virtual environments
- caches or build artifacts

## Data Locations

- `data/` contains real local databases and working data.
- `exports/` contains generated export files.
- `reports/` contains generated reports.
- `sample_data/` contains fake examples only.

If a file contains real user information, keep it out of GitHub.
