from app.services.report_filter_service import ReportFilterService


class FakeHistoryService:
    def __init__(self, reports):
        self._reports = reports

    def list_reports(self):
        return self._reports


REPORTS = [
    {
        "filename": "identity_audit_001.json",
        "report_type": "identity_audit",
        "status": "complete",
        "created_at": "2026-06-27",
    },
    {
        "filename": "identity_review_002.json",
        "report_type": "identity_review",
        "status": "review",
        "created_at": "2026-06-26",
    },
    {
        "filename": "identity_audit_003.json",
        "report_type": "identity_audit",
        "status": "review",
        "created_at": "2026-06-25",
    },
]


def test_empty_archive_returns_empty_results():
    service = ReportFilterService(
        FakeHistoryService([])
    )

    assert service.search() == []


def test_filter_by_report_type():
    service = ReportFilterService(
        FakeHistoryService(REPORTS)
    )

    results = service.search(report_type="identity_audit")

    assert len(results) == 2


def test_filter_by_status():
    service = ReportFilterService(
        FakeHistoryService(REPORTS)
    )

    results = service.search(status="review")

    assert len(results) == 2


def test_filter_by_filename():
    service = ReportFilterService(
        FakeHistoryService(REPORTS)
    )

    results = service.search(filename_contains="003")

    assert len(results) == 1
    assert results[0]["filename"] == "identity_audit_003.json"


def test_combined_filters():
    service = ReportFilterService(
        FakeHistoryService(REPORTS)
    )

    results = service.search(
        report_type="identity_audit",
        status="review",
    )

    assert len(results) == 1
    assert results[0]["filename"] == "identity_audit_003.json"


def test_limit_results():
    service = ReportFilterService(
        FakeHistoryService(REPORTS)
    )

    results = service.search(limit=2)

    assert len(results) == 2


def test_no_matches():
    service = ReportFilterService(
        FakeHistoryService(REPORTS)
    )

    assert service.search(report_type="missing") == []