from app.services.reporting_service import ReportingService


class FakeHistoryService:
    def __init__(self):
        self.reports = [
            {"filename": "newest.json", "created_at": "2026-06-28T10:00:00"},
            {"filename": "older.json", "created_at": "2026-06-27T10:00:00"},
        ]

    def list_reports(self):
        return self.reports

    def latest_report(self):
        return self.reports[0]

    def get_report(self, filename):
        for report in self.reports:
            if report["filename"] == filename:
                return report
        return None


class FakeSearchService:
    def __init__(self):
        self.last_call = None

    def search_reports(
        self,
        report_type=None,
        status=None,
        query=None,
        limit=None,
    ):
        self.last_call = {
            "report_type": report_type,
            "status": status,
            "query": query,
            "limit": limit,
        }
        return [{"filename": "matched.json"}]


class FakeDeleteService:
    def __init__(self):
        self.deleted_filename = None

    def delete_report(self, filename):
        self.deleted_filename = filename
        return True


class FakeExportService:
    def __init__(self):
        self.last_call = None

    def export_report(self, filename, destination):
        self.last_call = {
            "filename": filename,
            "destination": destination,
        }
        return {
            "filename": filename,
            "destination": destination,
            "exported": True,
        }


def make_service():
    history_service = FakeHistoryService()
    search_service = FakeSearchService()
    delete_service = FakeDeleteService()
    export_service = FakeExportService()

    service = ReportingService(
        history_service=history_service,
        search_service=search_service,
        delete_service=delete_service,
        export_service=export_service,
    )

    return service, history_service, search_service, delete_service, export_service


def test_lists_reports_from_history_service():
    service, history_service, _, _, _ = make_service()

    assert service.list_reports() == history_service.reports


def test_returns_latest_report_from_history_service():
    service, history_service, _, _, _ = make_service()

    assert service.latest_report() == history_service.reports[0]


def test_gets_report_by_filename_from_history_service():
    service, _, _, _, _ = make_service()

    assert service.get_report("older.json") == {
        "filename": "older.json",
        "created_at": "2026-06-27T10:00:00",
    }


def test_returns_none_when_report_is_missing():
    service, _, _, _, _ = make_service()

    assert service.get_report("missing.json") is None


def test_delegates_search_with_filters():
    service, _, search_service, _, _ = make_service()

    result = service.search_reports(
        report_type="identity",
        status="review",
        query="aphex",
        limit=10,
    )

    assert result == [{"filename": "matched.json"}]
    assert search_service.last_call == {
        "report_type": "identity",
        "status": "review",
        "query": "aphex",
        "limit": 10,
    }


def test_deletes_report_by_filename():
    service, _, _, delete_service, _ = make_service()

    result = service.delete_report("old.json")

    assert result is True
    assert delete_service.deleted_filename == "old.json"


def test_exports_report_to_destination():
    service, _, _, _, export_service = make_service()

    result = service.export_report("report.json", "exports/report.json")

    assert result == {
        "filename": "report.json",
        "destination": "exports/report.json",
        "exported": True,
    }
    assert export_service.last_call == {
        "filename": "report.json",
        "destination": "exports/report.json",
    }


def test_delegate_failures_are_not_swallowed():
    class BrokenHistoryService(FakeHistoryService):
        def list_reports(self):
            raise RuntimeError("archive unavailable")

    service = ReportingService(
        history_service=BrokenHistoryService(),
        search_service=FakeSearchService(),
        delete_service=FakeDeleteService(),
        export_service=FakeExportService(),
    )

    try:
        service.list_reports()
    except RuntimeError as error:
        assert str(error) == "archive unavailable"
    else:
        raise AssertionError("Expected RuntimeError")