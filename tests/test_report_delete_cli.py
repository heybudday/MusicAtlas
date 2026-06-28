from app.cli.report_delete import ReportDeleteCLI


class FakeDeleteService:
    def __init__(self, deleted=True):
        self.deleted = deleted
        self.requested = None

    def delete_report(self, filename):
        self.requested = filename
        return self.deleted


def test_delete_success(capsys):
    service = FakeDeleteService(True)
    cli = ReportDeleteCLI(service)

    result = cli.run("identity-report.json")

    captured = capsys.readouterr()

    assert result == 0
    assert service.requested == "identity-report.json"
    assert "Deleted report: identity-report.json" in captured.out


def test_delete_missing_report(capsys):
    service = FakeDeleteService(False)
    cli = ReportDeleteCLI(service)

    result = cli.run("missing.json")

    captured = capsys.readouterr()

    assert result == 1
    assert service.requested == "missing.json"
    assert "Report not found: missing.json" in captured.out