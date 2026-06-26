import sys
from pathlib import Path

from database import Base, engine
from importers.discogs_csv import import_discogs_csv


def initialize_database():
    """Create the SQLite database if it doesn't already exist."""
    Base.metadata.create_all(engine)


def run_import(csv_path: str):
    """Import a Discogs CSV export and print a summary."""
    result = import_discogs_csv(csv_path)
    summary = result["summary"]

    print("Import complete.")
    print(f"Archived copy: {result['archived_path']}")
    print(f"Rows: {summary['rows']}")
    print(f"Unique releases: {summary['unique_releases']}")
    print(f"Artists: {summary['artists']}")
    print(f"Labels: {summary['labels']}")


def main():
    initialize_database()

    if len(sys.argv) == 3 and sys.argv[1] == "import":
        run_import(sys.argv[2])
        return

    print("=" * 40)
    print("Music Atlas")
    print("=" * 40)

    project_root = Path(__file__).resolve().parent.parent

    print(f"Project: {project_root}")
    print("Database initialized.")
    print("Ready.")


if __name__ == "__main__":
    main()