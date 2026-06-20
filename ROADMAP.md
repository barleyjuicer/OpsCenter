# Roadmap

## Current Goal

Provide a central local operations platform for organizing projects, tasks, executive metrics, resources, and decision-support activity.

## Near-Term Improvements

- Improve project and task workflows.
- Add richer status reporting and dashboard drilldowns.
- Add export flows that write only to `exports/`.
- Add report generation that writes only to `reports/`.
- Add import support for fake/sample data.

## Future Modules

- Knowledge management
- Job tracking
- Study tracking
- Health tracking
- Financial tracking
- Notes and decision logs
- Risk and dependency tracking

## Repository Safety

- Keep real user databases in `data/` only.
- Keep generated exports in `exports/` only.
- Keep generated reports in `reports/` only.
- Commit fake examples only from `sample_data/`.
- Never commit PHI, PII, logs, screenshots, databases, generated exports, or generated reports.

## Development Approach

This is an AI-assisted project directed by the repository owner. AI can help draft implementation, tests, and documentation, while the owner reviews the work and controls what is committed, released, and shared.
