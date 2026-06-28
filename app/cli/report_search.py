from __future__ import annotations

import argparse

from app.services.report_archive_loader import ReportArchiveLoader
from app.services.report_filter_service import ReportFilterService
from app.services.report_history_service import ReportHistoryService


class ReportSearchCLI:
    def __init__(self):
        loader = ReportArchiveLoader()
        history = ReportHistoryService(loader)
        self.service = ReportFilterService(history)

    def run(self, argv=None):
        parser = argparse.ArgumentParser(
            description="Search archived reports."
        )

        parser.add_argument(
            "--type",
            dest="report_type",
        )

        parser.add_argument(
            "--status",
        )

        parser.add_argument(
            "--contains",
            dest="filename_contains",
        )

        parser.add_argument(
            "--limit",
            type=int,
        )

        args = parser.parse_args(argv)

        reports = self.service.search(
            report_type=args.report_type,
            status=args.status,
            filename_contains=args.filename_contains,
            limit=args.limit,
        )

        print(f"Found {len(reports)} report(s).")

        if not reports:
            return

        print()

        for report in reports:
            print(report.get("created_at", ""))
            print(report.get("report_type", ""))
            print(report.get("status", ""))
            print(report.get("filename", ""))
            print()


def main():
    ReportSearchCLI().run()


if __name__ == "__main__":
    main()