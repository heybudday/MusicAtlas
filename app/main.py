import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from app.database import Base, engine
from app.importers.discogs_csv import import_discogs_csv
from app.repositories.identity_resolution_repository import (
    IdentityResolutionRepository,
)
from app.services.identity_report_service import IdentityReportService


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


def run_identity_report():
    """Generate and display the identity resolution report."""
    repository = IdentityResolutionRepository()
    service = IdentityReportService(repository=repository)

    report = service.generate_report()

    print("Identity Resolution Report")
    print("=" * 40)
    print(f"Total: {report['total']}")
    print(f"Resolved: {report['resolved']}")
    print(f"Review: {report['review']}")
    print(f"Unresolved: {report['unresolved']}")
    print(f"Resolution Rate: {report['resolution_rate']:.1%}")
    print(f"Review Rate: {report['review_rate']:.1%}")
    print(f"Average Confidence: {report['average_confidence']:.2f}")


def main():
    initialize_database()

    if len(sys.argv) == 3 and sys.argv[1] == "import":
        run_import(sys.argv[2])
        return

    if len(sys.argv) == 2 and sys.argv[1] == "identity-report":
        run_identity_report()
        return

    print("=" * 40)
    print("Music Atlas")
    print("=" * 40)
    print(f"Project: {project_root}")
    print("Database initialized.")


if __name__ == "__main__":
    main()