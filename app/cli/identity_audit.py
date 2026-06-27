from __future__ import annotations

import argparse

from app.database import SessionLocal
from app.services.identity_audit_exporter import IdentityAuditExporter
from app.services.identity_audit_runner import IdentityAuditRunner


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Music Atlas identity audit."
    )

    parser.add_argument(
        "--format",
        choices=["json", "csv", "both"],
        default=None,
        help="Export report format.",
    )

    parser.add_argument(
        "--output-dir",
        default="reports",
        help="Directory for exported reports.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 41)
    print("Music Atlas Identity Audit")
    print("=" * 41)
    print()

    session = SessionLocal()

    try:
        runner = IdentityAuditRunner(session)
        audit_output = runner.run_all()

        summary, results = _split_audit_output(audit_output)

        print(f"Processed:   {summary['processed']}")
        print(f"Successful: {summary['success']}")
        print(f"Review:     {summary['review']}")
        print(f"Failed:     {summary['failed']}")

        if args.format:
            exporter = IdentityAuditExporter(args.output_dir)
            exported_files = exporter.export(
                summary=summary,
                results=results,
                export_format=args.format,
            )

            print()
            print("Exported:")

            for path in exported_files:
                print(f"- {path}")

        print()
        print("Done.")

    finally:
        session.close()


def _split_audit_output(audit_output):
    if (
        isinstance(audit_output, dict)
        and "summary" in audit_output
        and "results" in audit_output
    ):
        return audit_output["summary"], audit_output["results"]

    return audit_output, []


if __name__ == "__main__":
    main()