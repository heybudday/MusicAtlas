from __future__ import annotations


class ReportHistoryService:
    """
    Provides convenient access to archived reports.
    """

    def __init__(self, loader):
        self.loader = loader

    def list_reports(self, limit=None):
        """
        Return archived reports sorted newest first.
        """
        reports = sorted(
            self.loader.load_reports(),
            key=lambda report: report["created_at"],
            reverse=True,
        )

        if limit is not None:
            return reports[:limit]

        return reports

    def latest_report(self):
        """
        Return the newest archived report, or None if no reports exist.
        """
        reports = self.list_reports(limit=1)
        return reports[0] if reports else None

    def get_report(self, archive_name):
        """
        Return a report matching the given archive filename, or None.
        """
        for report in self.loader.load_reports():
            if report["archive_name"] == archive_name:
                return report

        return None