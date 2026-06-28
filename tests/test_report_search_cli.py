from app.cli.report_search import ReportSearchCLI


class FakeService:
    def __init__(self, reports):
        self.reports = reports
        self.kwargs = None

    def search(self, **kwargs):
        self.kwargs = kwargs
        return self.reports


REPORTS = [
    {
        "filename": "identity_audit.json",
        "report_type": "identity_audit",
        "status": "complete",
        "created_at": "2026-06-27",
    }
]


def build_cli(reports):
    cli = ReportSearchCLI.__new__(ReportSearchCLI)
    cli.service = FakeService(reports)
    return cli


def test_no_results(capsys):
    cli = build_cli([])

    cli.run([])

    output = capsys.readouterr().out

    assert "Found 0 report(s)." in output


def test_search_by_type():
    cli = build_cli(REPORTS)

    cli.run(["--type", "identity_audit"])

    assert cli.service.kwargs["report_type"] == "identity_audit"


def test_search_by_status():
    cli = build_cli(REPORTS)

    cli.run(["--status", "complete"])

    assert cli.service.kwargs["status"] == "complete"


def test_combined_filters():
    cli = build_cli(REPORTS)

    cli.run(
        [
            "--type",
            "identity_audit",
            "--status",
            "complete",
            "--contains",
            "audit",
            "--limit",
            "5",
        ]
    )

    assert cli.service.kwargs == {
        "report_type": "identity_audit",
        "status": "complete",
        "filename_contains": "audit",
        "limit": 5,
    }


def test_output_contains_report_information(capsys):
    cli = build_cli(REPORTS)

    cli.run([])

    output = capsys.readouterr().out

    assert "identity_audit" in output
    assert "complete" in output
    assert "identity_audit.json" in output


def test_limit_option():
    cli = build_cli(REPORTS)

    cli.run(["--limit", "1"])

    assert cli.service.kwargs["limit"] == 1