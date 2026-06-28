from __future__ import annotations

from app.services.report_delete_service import ReportDeleteService


class ReportDeleteCLI:
    """
    Command-line interface for deleting archived reports.
    """

    def __init__(self, delete_service: ReportDeleteService):
        self.delete_service = delete_service

    def run(self, filename: str) -> int:
        """
        Delete a report by filename.

        Returns:
            0 if deleted successfully.
            1 if the report was not found.
        """
        deleted = self.delete_service.delete_report(filename)

        if deleted:
            print(f"Deleted report: {filename}")
            return 0

        print(f"Report not found: {filename}")
        return 1