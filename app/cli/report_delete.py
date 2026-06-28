from __future__ import annotations

import argparse

from app.services.report_archive_loader import ReportArchiveLoader
from app.services.report_delete_service import ReportDeleteService
from app.services.report_history_service import ReportHistoryService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="report-delete",
        description="Delete an archived report.",
    )
    parser.add_argument("filename", help="Report filename to delete")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    loader = ReportArchiveLoader()
    history = ReportHistoryService(loader)
    service = ReportDeleteService(history)

    if service.delete_report(args.filename):
        print(f"Deleted report: {args.filename}")
        return 0

    print(f"Report not found: {args.filename}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())