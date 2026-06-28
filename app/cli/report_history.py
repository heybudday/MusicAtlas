from __future__ import annotations


class ReportHistoryCLI:
    """
    Simple CLI wrapper for browsing archived reports.
    """

    def __init__(self, archive_service):
        self.archive_service = archive_service

    def list_reports(self, limit=None):
        """
        Return archived reports in newest-first order.

        If a limit is provided, only that many reports are returned.
        """
        reports = list(self.archive_service.list_reports())

        reports.sort(
            key=lambda report: report.get("created_at", ""),
            reverse=True,
        )

        if limit is not None:
            reports = reports[:limit]

        return reports

    def display_reports(self, limit=None):
        """
        Print a human-readable list of archived reports.
        """
        reports = self.list_reports(limit)

        if not reports:
            print("No archived reports found.")
            return

        print("Archived Reports")
        print()

        for report in reports:
            created = report.get("created_at", "Unknown")
            filename = report.get("filename", "Unknown")

            print(created)
            print(filename)
            print()