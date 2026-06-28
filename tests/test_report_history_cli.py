from app.cli.report_history import ReportHistoryCLI


class FakeArchiveService:
    def __init__(self, reports):
        self._reports = reports

    def list_reports(self):
        return list(self._reports)


def test_empty_archive():
    cli = ReportHistoryCLI(FakeArchiveService([]))

    assert cli.list_reports() == []


def test_single_report():
    reports = [
        {
            "filename": "report1.json",
            "created_at": "2026-06-27 10:00",
        }
    ]

    cli = ReportHistoryCLI(FakeArchiveService(reports))

    assert cli.list_reports() == reports


def test_multiple_reports_sorted_newest_first():
    reports = [
        {
            "filename": "old.json",
            "created_at": "2026-06-25 09:00",
        },
        {
            "filename": "new.json",
            "created_at": "2026-06-27 12:00",
        },
        {
            "filename": "mid.json",
            "created_at": "2026-06-26 11:00",
        },
    ]

    cli = ReportHistoryCLI(FakeArchiveService(reports))

    result = cli.list_reports()

    assert [r["filename"] for r in result] == [
        "new.json",
        "mid.json",
        "old.json",
    ]


def test_limit():
    reports = [
        {"filename": "3.json", "created_at": "2026-06-27 12:00"},
        {"filename": "2.json", "created_at": "2026-06-26 12:00"},
        {"filename": "1.json", "created_at": "2026-06-25 12:00"},
    ]

    cli = ReportHistoryCLI(FakeArchiveService(reports))

    result = cli.list_reports(limit=2)

    assert len(result) == 2
    assert result[0]["filename"] == "3.json"
    assert result[1]["filename"] == "2.json"


def test_display_reports(capsys):
    reports = [
        {
            "filename": "report.json",
            "created_at": "2026-06-27 14:35",
        }
    ]

    cli = ReportHistoryCLI(FakeArchiveService(reports))
    cli.display_reports()

    output = capsys.readouterr().out

    assert "Archived Reports" in output
    assert "report.json" in output
    assert "2026-06-27 14:35" in output


def test_display_empty_archive(capsys):
    cli = ReportHistoryCLI(FakeArchiveService([]))
    cli.display_reports()

    output = capsys.readouterr().out

    assert output.strip() == "No archived reports found."