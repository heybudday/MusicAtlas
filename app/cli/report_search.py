from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.services.report_history_service import ReportHistoryService
from app.services.report_search_service import ReportSearchService


class CliReportArchiveLoader:
    def __init__(self, archive_dir: Path):
        self.archive_dir = archive_dir

    def load_reports(self) -> list[dict]:
        if not self.archive_dir.exists():
            return []

        reports = []

        for path in sorted(self.archive_dir.glob("*.json")):
            report = json.loads(path.read_text(encoding="utf-8"))
            report.setdefault("filename", path.name)
            report.setdefault("created_at", 0)
            reports.append(report)

        return reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search archived Music Atlas reports.",
    )

    parser.add_argument(
        "contains",
        nargs="?",
        default=None,
        help="Text to search for in archived reports.",
    )
    parser.add_argument(
        "--archive-dir",
        default="data/reports",
        help="Directory containing archived report JSON files.",
    )
    parser.add_argument(
        "--report-type",
        default=None,
        help="Filter results by report type.",
    )

    return parser


def format_result(report: dict) -> str:
    filename = report.get("filename", "unknown")
    report_type = report.get("report_type", "unknown")
    artist = report.get("artist") or report.get("name") or "Unknown artist"

    return f"{filename} | {report_type} | {artist}"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    loader = CliReportArchiveLoader(Path(args.archive_dir))
    history_service = ReportHistoryService(loader)
    search_service = ReportSearchService(history_service)

    results = search_service.search(
        report_type=args.report_type,
        contains=args.contains,
    )

    if not results:
        print("No matching reports found.")
        return 0

    for report in results:
        print(format_result(report))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())