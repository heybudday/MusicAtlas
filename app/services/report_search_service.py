from __future__ import annotations


class ReportSearchService:
    """
    Provides simple searching across archived reports.
    """

    def __init__(self, history_service):
        self.history_service = history_service

    def search(
        self,
        report_type=None,
        contains=None,
    ):
        reports = self.history_service.list_reports()

        results = []

        for report in reports:
            if report_type:
                if report.get("report_type") != report_type:
                    continue

            if contains:
                text = str(report).lower()
                if contains.lower() not in text:
                    continue

            results.append(report)

        return results