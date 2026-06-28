from app.cli.report_delete import main


class FakeDeleteService:
    def __init__(self, deleted):
        self.deleted = deleted
        self.called_with = None

    def delete_report(self, filename):
        self.called_with = filename
        return self.deleted


class FakeHistoryService:
    pass


class FakeLoader:
    pass


def test_delete_success(monkeypatch, capsys):
    service = FakeDeleteService(True)

    monkeypatch.setattr(
        "app.cli.report_delete.ReportArchiveLoader",
        lambda: FakeLoader(),
    )
    monkeypatch.setattr(
        "app.cli.report_delete.ReportHistoryService",
        lambda loader: FakeHistoryService(),
    )
    monkeypatch.setattr(
        "app.cli.report_delete.ReportDeleteService",
        lambda history: service,
    )

    result = main(["example.json"])

    captured = capsys.readouterr()

    assert result == 0
    assert service.called_with == "example.json"
    assert "Deleted report: example.json" in captured.out


def test_delete_missing(monkeypatch, capsys):
    service = FakeDeleteService(False)

    monkeypatch.setattr(
        "app.cli.report_delete.ReportArchiveLoader",
        lambda: FakeLoader(),
    )
    monkeypatch.setattr(
        "app.cli.report_delete.ReportHistoryService",
        lambda loader: FakeHistoryService(),
    )
    monkeypatch.setattr(
        "app.cli.report_delete.ReportDeleteService",
        lambda history: service,
    )

    result = main(["missing.json"])

    captured = capsys.readouterr()

    assert result == 1
    assert service.called_with == "missing.json"
    assert "Report not found: missing.json" in captured.out