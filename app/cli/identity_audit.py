from __future__ import annotations

import argparse

from app.database import SessionLocal
from app.services.identity_audit_dashboard import IdentityAuditDashboard
from app.services.identity_audit_exporter import IdentityAuditExporter
from app.services.identity_audit_runner import IdentityAuditRunner


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Music Atlas identity audit."
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=["run", "dashboard"],
        default="run",
        help="Command to run.",
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

    session = SessionLocal()

    try:
        runner = IdentityAuditRunner(session)
        audit_output = runner.run_all()

        summary, results = _split_audit_output(audit_output)

        if args.command == "dashboard":
            dashboard = IdentityAuditDashboard().summary(results)
            _print_dashboard(dashboard)
            return

        _print_audit_summary(summary)

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


def _print_audit_summary(summary):
    print("=" * 41)
    print("Music Atlas Identity Audit")
    print("=" * 41)
    print()

    print(f"Processed:   {summary['processed']}")
    print(f"Successful: {summary['success']}")
    print(f"Review:     {summary['review']}")
    print(f"Failed:     {summary['failed']}")


def _print_dashboard(summary):
    print("=" * 41)
    print("Identity Audit Dashboard")
    print("=" * 41)
    print()

    print(f"Artists audited: {summary['total']}")
    print()
    print(f"Passed:         {summary['passed']}")
    print(f"Needs Review:   {summary['review']}")
    print(f"Failed:         {summary['failed']}")
    print()

    print("Confidence")
    print(f"High:           {summary['confidence']['high']}")
    print(f"Medium:         {summary['confidence']['medium']}")
    print(f"Low:            {summary['confidence']['low']}")
    print()

    print("Provider Success")

    if summary["providers"]:
        for provider, count in summary["providers"].items():
            print(f"{provider}: {count}")
    else:
        print("None")
    print()

    print("Common Issues")

    if summary["issues"]:
        for issue, count in summary["issues"].items():
            print(f"{issue}: {count}")
    else:
        print("None")
    print()

    print(f"Last Audit: {summary['last_audit']}")


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