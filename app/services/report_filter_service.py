from __future__ import annotations


class ReportFilterService:
    """
    Provides filtering capabilities over archived report metadata.
    """

    def __init__(self, history_service):
        self.history_service = history_service

    def search(
        self,
        report_type=None,
        status=None,
        filename_contains=None,
        limit=None,
    ):
        reports = list(self.history_service.list_reports())

        if report_type:
            reports = [
                report
                for report in reports
                if report.get("report_type") == report_type
            ]

        if status:
            reports = [
                report
                for report in reports
                if report.get("status") == status
            ]

        if filename_contains:
            search = filename_contains.lower()

            reports = [
                report
                for report in reports
                if search in report.get("filename", "").lower()
            ]

        if limit is not None:
            reports = reports[:limit]

        return reports