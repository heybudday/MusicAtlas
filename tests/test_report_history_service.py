from app.services.report_history_service import ReportHistoryService


class FakeLoader:
    def __init__(self, reports):
        self._reports = reports

    def load_reports(self):
        return self._reports


def test_empty_archive_returns_empty_list():
    service = ReportHistoryService(FakeLoader([]))

    assert service.list_reports() == []
    assert service.latest_report() is None
    assert service.get_report("anything.json") is None


def test_reports_are_sorted_newest_first():
    reports = [
        {
            "archive_name": "old.json",
            "created_at": "2026-06-01T10:00:00",
        },
        {
            "archive_name": "new.json",
            "created_at": "2026-06-05T10:00:00",
        },
        {
            "archive_name": "middle.json",
            "created_at": "2026-06-03T10:00:00",
        },
    ]

    service = ReportHistoryService(FakeLoader(reports))

    result = service.list_reports()

    assert [r["archive_name"] for r in result] == [
        "new.json",
        "middle.json",
        "old.json",
    ]


def test_limit_returns_requested_number():
    reports = [
        {
            "archive_name": f"report{i}.json",
            "created_at": f"2026-06-{i:02d}T10:00:00",
        }
        for i in range(1, 6)
    ]

    service = ReportHistoryService(FakeLoader(reports))

    result = service.list_reports(limit=2)

    assert len(result) == 2
    assert result[0]["archive_name"] == "report5.json"
    assert result[1]["archive_name"] == "report4.json"


def test_latest_report_returns_newest():
    reports = [
        {
            "archive_name": "old.json",
            "created_at": "2026-06-01T10:00:00",
        },
        {
            "archive_name": "new.json",
            "created_at": "2026-06-05T10:00:00",
        },
    ]

    service = ReportHistoryService(FakeLoader(reports))

    assert service.latest_report()["archive_name"] == "new.json"


def test_get_report_returns_requested_report():
    reports = [
        {
            "archive_name": "one.json",
            "created_at": "2026-06-01T10:00:00",
        },
        {
            "archive_name": "two.json",
            "created_at": "2026-06-02T10:00:00",
        },
    ]

    service = ReportHistoryService(FakeLoader(reports))

    report = service.get_report("two.json")

    assert report is not None
    assert report["archive_name"] == "two.json"


def test_get_report_returns_none_for_unknown_report():
    reports = [
        {
            "archive_name": "one.json",
            "created_at": "2026-06-01T10:00:00",
        }
    ]

    service = ReportHistoryService(FakeLoader(reports))

    assert service.get_report("missing.json") is None