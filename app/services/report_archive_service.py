from __future__ import annotations

from datetime import datetime


class ReportArchiveService:
    """
    Maintains an in-memory archive of generated reports.
    """

    def __init__(self):
        self._reports = []
        self._next_id = 1

    def archive(
        self,
        report_type: str,
        filename: str,
        path: str,
        record_count: int,
    ):
        entry = {
            "id": self._next_id,
            "report_type": report_type,
            "filename": filename,
            "path": path,
            "record_count": record_count,
            "generated_at": datetime.utcnow(),
        }

        self._reports.append(entry)
        self._next_id += 1

        return entry

    def list_reports(self):
        return sorted(
            self._reports,
            key=lambda report: report["generated_at"],
            reverse=True,
        )

    def get(self, report_id):
        for report in self._reports:
            if report["id"] == report_id:
                return report
        return None

    def get_by_filename(self, filename):
        for report in self._reports:
            if report["filename"] == filename:
                return report
        return None