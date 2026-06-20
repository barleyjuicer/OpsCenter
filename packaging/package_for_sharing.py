from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = PROJECT_ROOT.parent / "OpsCenter-share.zip"
SKIP_DIRS = {
    ".agents",
    ".codex",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".streamlit",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "logs",
    "outputs",
    "work",
}
PRIVATE_DIRS = {"data", "exports", "reports"}
ALLOW_PRIVATE_PLACEHOLDERS = {"README.md", ".gitkeep"}
SKIP_SUFFIXES = {
    ".db",
    ".sqlite",
    ".sqlite3",
    ".db-journal",
    ".pyc",
    ".pyo",
    ".log",
    ".csv",
    ".xlsx",
    ".xls",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".exe",
    ".msi",
    ".dmg",
}


def should_skip(path: Path) -> bool:
    relative = path.relative_to(PROJECT_ROOT)
    if any(part in SKIP_DIRS for part in relative.parts):
        return True
    if relative.parts and relative.parts[0] == "sample_data":
        return False
    if relative.parts and relative.parts[0] in PRIVATE_DIRS:
        return path.name not in ALLOW_PRIVATE_PLACEHOLDERS
    return path.suffix.lower() in SKIP_SUFFIXES


def main() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with ZipFile(ZIP_PATH, "w", ZIP_DEFLATED) as archive:
        for path in PROJECT_ROOT.rglob("*"):
            if path.is_file() and not should_skip(path):
                archive.write(path, Path(PROJECT_ROOT.name) / path.relative_to(PROJECT_ROOT))

    print(f"Done: {ZIP_PATH}")


if __name__ == "__main__":
    main()
