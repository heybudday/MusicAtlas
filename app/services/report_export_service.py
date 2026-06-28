import csv
import io
import json


class ReportExportService:
    """
    Exports report history into various text formats.
    """

    def __init__(self, history_service):
        self.history_service = history_service

    def export_json(self):
        reports = self.history_service.list_reports()
        return json.dumps(reports, indent=2, sort_keys=True)

    def export_csv(self):
        reports = self.history_service.list_reports()

        if not reports:
            return ""

        fieldnames = sorted(
            {
                key
                for report in reports
                for key in report.keys()
            }
        )

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        writer.writeheader()

        for report in reports:
            writer.writerow(report)

        return buffer.getvalue()

    def export_markdown(self):
        reports = self.history_service.list_reports()

        if not reports:
            return ""

        columns = sorted(
            {
                key
                for report in reports
                for key in report.keys()
            }
        )

        lines = [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
        ]

        for report in reports:
            lines.append(
                "| "
                + " | ".join(str(report.get(column, "")) for column in columns)
                + " |"
            )

        return "\n".join(lines)

    def export_report_json(self, filename):
        report = self.history_service.get_report(filename)

        if report is None:
            return None

        return json.dumps(report, indent=2, sort_keys=True)

    def export_report_csv(self, filename):
        report = self.history_service.get_report(filename)

        if report is None:
            return None

        fieldnames = sorted(report.keys())

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(report)

        return buffer.getvalue()