from app.services.report_search_service import ReportSearchService


class FakeHistoryService:
    def __init__(self, reports):
        self._reports = reports

    def list_reports(self):
        return self._reports


def test_returns_all_when_no_filters():
    reports = [
        {"filename": "a.json", "report_type": "identity"},
        {"filename": "b.json", "report_type": "audit"},
    ]

    service = ReportSearchService(FakeHistoryService(reports))

    assert service.search() == reports


def test_filter_by_report_type():
    reports = [
        {"filename": "a.json", "report_type": "identity"},
        {"filename": "b.json", "report_type": "audit"},
        {"filename": "c.json", "report_type": "identity"},
    ]

    service = ReportSearchService(FakeHistoryService(reports))

    result = service.search(report_type="identity")

    assert len(result) == 2
    assert all(r["report_type"] == "identity" for r in result)


def test_text_search():
    reports = [
        {
            "filename": "one.json",
            "report_type": "identity",
            "artist": "Jeff Mills",
        },
        {
            "filename": "two.json",
            "report_type": "identity",
            "artist": "Carl Cox",
        },
    ]

    service = ReportSearchService(FakeHistoryService(reports))

    result = service.search(contains="Jeff")

    assert len(result) == 1
    assert result[0]["artist"] == "Jeff Mills"


def test_combined_filters():
    reports = [
        {
            "filename": "one.json",
            "report_type": "identity",
            "artist": "Jeff Mills",
        },
        {
            "filename": "two.json",
            "report_type": "audit",
            "artist": "Jeff Mills",
        },
    ]

    service = ReportSearchService(FakeHistoryService(reports))

    result = service.search(
        report_type="identity",
        contains="Jeff",
    )

    assert len(result) == 1
    assert result[0]["filename"] == "one.json"


def test_no_matches():
    reports = [
        {"filename": "a.json", "report_type": "identity"},
    ]

    service = ReportSearchService(FakeHistoryService(reports))

    assert service.search(report_type="audit") == []