from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.report_archive_loader import ReportArchiveLoader
from app.services.report_history_service import ReportHistoryService


DEFAULT_ARCHIVE_DIRECTORY = Path("data/reports/archive")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="View one archived Music Atlas report.",
    )
    parser.add_argument(
        "filename",
        help="Archived report filename to view.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    loader = ReportArchiveLoader(DEFAULT_ARCHIVE_DIRECTORY)
    service = ReportHistoryService(loader)
    report = service.get_report(args.filename)

    if report is None:
        print(f"Report not found: {args.filename}")
        return 1

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())