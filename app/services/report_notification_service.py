from __future__ import annotations


class ReportNotificationService:
    """
    Builds lightweight notifications from archived report metadata.
    """

    def __init__(self, history_service):
        self.history_service = history_service

    def latest_notification(self):
        report = self.history_service.latest_report()

        if report is None:
            return None

        return self.notification_for_report(report)

    def notification_for_report(self, report):
        filename = report.get("filename", "unknown")
        report_type = report.get("report_type", "unknown")
        created_at = report.get("created_at")

        summary = report.get("summary") or {}
        total = summary.get("total", 0)
        resolved = summary.get("resolved", 0)
        review = summary.get("review", 0)
        unresolved = summary.get("unresolved", 0)

        severity = self._severity(review, unresolved)

        message = (
            f"{report_type} report {filename}: "
            f"{total} total, {resolved} resolved, "
            f"{review} review, {unresolved} unresolved."
        )

        return {
            "filename": filename,
            "report_type": report_type,
            "created_at": created_at,
            "severity": severity,
            "message": message,
            "counts": {
                "total": total,
                "resolved": resolved,
                "review": review,
                "unresolved": unresolved,
            },
        }

    def notification_digest(self):
        reports = self.history_service.list_reports()

        return [self.notification_for_report(report) for report in reports]

    def actionable_notifications(self):
        return [
            notification
            for notification in self.notification_digest()
            if notification["severity"] in {"warning", "critical"}
        ]

    def _severity(self, review, unresolved):
        if unresolved > 0:
            return "critical"

        if review > 0:
            return "warning"

        return "info"