from __future__ import annotations


class ReportingService:
    """
    High-level integration service for report workflows.
    """

    def __init__(
        self,
        history_service,
        search_service,
        delete_service,
        export_service,
    ):
        self.history_service = history_service
        self.search_service = search_service
        self.delete_service = delete_service
        self.export_service = export_service

    def list_reports(self):
        return self.history_service.list_reports()

    def latest_report(self):
        return self.history_service.latest_report()

    def get_report(self, filename):
        return self.history_service.get_report(filename)

    def search_reports(
        self,
        report_type=None,
        status=None,
        query=None,
        limit=None,
    ):
        return self.search_service.search_reports(
            report_type=report_type,
            status=status,
            query=query,
            limit=limit,
        )

    def delete_report(self, filename):
        return self.delete_service.delete_report(filename)

    def export_report(self, filename, destination):
        return self.export_service.export_report(filename, destination)