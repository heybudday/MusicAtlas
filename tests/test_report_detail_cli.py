from __future__ import annotations

import json

from app.cli.report_detail import main


def test_prints_report_by_filename(monkeypatch, capsys):
    class FakeHistoryService:
        def __init__(self, loader):
            self.loader = loader

        def get_report(self, filename):
            assert filename == "identity-report.json"
            return {
                "filename": "identity-report.json",
                "report_type": "identity",
                "summary": {"total": 2},
            }

    monkeypatch.setattr(
        "app.cli.report_detail.ReportHistoryService",
        FakeHistoryService,
    )

    exit_code = main(["identity-report.json"])

    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output == {
        "filename": "identity-report.json",
        "report_type": "identity",
        "summary": {"total": 2},
    }


def test_returns_error_when_report_not_found(monkeypatch, capsys):
    class FakeHistoryService:
        def __init__(self, loader):
            self.loader = loader

        def get_report(self, filename):
            assert filename == "missing.json"
            return None

    monkeypatch.setattr(
        "app.cli.report_detail.ReportHistoryService",
        FakeHistoryService,
    )

    exit_code = main(["missing.json"])

    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Report not found: missing.json" in output