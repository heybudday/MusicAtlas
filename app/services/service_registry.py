from __future__ import annotations

from app.services.report_archive_service import ReportArchiveService
from app.services.report_delete_service import ReportDeleteService
from app.services.report_export_service import ReportExportService
from app.services.report_history_service import ReportHistoryService
from app.services.report_search_service import ReportSearchService
from app.ui.command_registry import CommandRegistry


class ServiceRegistry:
    """
    Central registry for application services.

    This class wires services together so CLI commands and future
    interfaces don't need to know how everything is constructed.
    """

    def __init__(
        self,
        *,
        archive_service: ReportArchiveService | None = None,
        history_service: ReportHistoryService | None = None,
        search_service: ReportSearchService | None = None,
        export_service: ReportExportService | None = None,
        delete_service: ReportDeleteService | None = None,
        command_registry: CommandRegistry | None = None,
    ):
        self.archive_service = archive_service
        self.history_service = history_service
        self.search_service = search_service
        self.export_service = export_service
        self.delete_service = delete_service
        self.command_registry = command_registry or CommandRegistry()

    def get(self, name: str):
        """
        Return a registered service.

        Raises:
            KeyError if the service does not exist.
        """
        try:
            return getattr(self, name)
        except AttributeError as exc:
            raise KeyError(name) from exc

    def available_services(self):
        """
        Return a sorted list of registered service names.
        """
        services = []

        for name, value in vars(self).items():
            if name == "command_registry":
                continue

            if value is not None:
                services.append(name)

        return sorted(services)