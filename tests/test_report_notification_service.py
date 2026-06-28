from app.services.report_notification_service import ReportNotificationService


class FakeHistoryService:
    def __init__(self, reports):
        self._reports = reports

    def list_reports(self):
        return self._reports

    def latest_report(self):
        if not self._reports:
            return None

        return self._reports[0]


def test_latest_notification_returns_none_when_no_reports():
    service = ReportNotificationService(FakeHistoryService([]))

    assert service.latest_notification() is None


def test_latest_notification_for_clean_report_is_info():
    reports = [
        {
            "filename": "identity-001.json",
            "report_type": "identity",
            "created_at": "2026-06-28T10:00:00",
            "summary": {
                "total": 10,
                "resolved": 10,
                "review": 0,
                "unresolved": 0,
            },
        }
    ]

    service = ReportNotificationService(FakeHistoryService(reports))

    result = service.latest_notification()

    assert result == {
        "filename": "identity-001.json",
        "report_type": "identity",
        "created_at": "2026-06-28T10:00:00",
        "severity": "info",
        "message": (
            "identity report identity-001.json: "
            "10 total, 10 resolved, 0 review, 0 unresolved."
        ),
        "counts": {
            "total": 10,
            "resolved": 10,
            "review": 0,
            "unresolved": 0,
        },
    }


def test_review_items_create_warning_notification():
    reports = [
        {
            "filename": "identity-002.json",
            "report_type": "identity",
            "summary": {
                "total": 8,
                "resolved": 6,
                "review": 2,
                "unresolved": 0,
            },
        }
    ]

    service = ReportNotificationService(FakeHistoryService(reports))

    result = service.latest_notification()

    assert result["severity"] == "warning"
    assert result["counts"]["review"] == 2


def test_unresolved_items_create_critical_notification():
    reports = [
        {
            "filename": "identity-003.json",
            "report_type": "identity",
            "summary": {
                "total": 8,
                "resolved": 5,
                "review": 2,
                "unresolved": 1,
            },
        }
    ]

    service = ReportNotificationService(FakeHistoryService(reports))

    result = service.latest_notification()

    assert result["severity"] == "critical"
    assert result["counts"]["unresolved"] == 1


def test_notification_digest_returns_all_reports():
    reports = [
        {
            "filename": "a.json",
            "report_type": "identity",
            "summary": {
                "total": 2,
                "resolved": 2,
                "review": 0,
                "unresolved": 0,
            },
        },
        {
            "filename": "b.json",
            "report_type": "identity",
            "summary": {
                "total": 2,
                "resolved": 1,
                "review": 1,
                "unresolved": 0,
            },
        },
    ]

    service = ReportNotificationService(FakeHistoryService(reports))

    result = service.notification_digest()

    assert len(result) == 2
    assert result[0]["filename"] == "a.json"
    assert result[1]["filename"] == "b.json"


def test_actionable_notifications_excludes_info_notifications():
    reports = [
        {
            "filename": "clean.json",
            "report_type": "identity",
            "summary": {
                "total": 1,
                "resolved": 1,
                "review": 0,
                "unresolved": 0,
            },
        },
        {
            "filename": "review.json",
            "report_type": "identity",
            "summary": {
                "total": 1,
                "resolved": 0,
                "review": 1,
                "unresolved": 0,
            },
        },
        {
            "filename": "unresolved.json",
            "report_type": "identity",
            "summary": {
                "total": 1,
                "resolved": 0,
                "review": 0,
                "unresolved": 1,
            },
        },
    ]

    service = ReportNotificationService(FakeHistoryService(reports))

    result = service.actionable_notifications()

    assert [notification["filename"] for notification in result] == [
        "review.json",
        "unresolved.json",
    ]