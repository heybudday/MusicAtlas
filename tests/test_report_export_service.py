import json

from app.services.report_export_service import ReportExportService


class FakeHistoryService:
    def __init__(self, reports):
        self._reports = reports

    def list_reports(self):
        return self._reports

    def get_report(self, filename):
        for report in self._reports:
            if report.get("filename") == filename:
                return report
        return None


def sample_reports():
    return [
        {
            "filename": "report1.json",
            "report_type": "identity",
            "created_at": "2026-06-28",
        },
        {
            "filename": "report2.json",
            "report_type": "audit",
            "created_at": "2026-06-27",
        },
    ]


def test_export_json():
    service = ReportExportService(FakeHistoryService(sample_reports()))

    exported = service.export_json()
    data = json.loads(exported)

    assert len(data) == 2
    assert data[0]["filename"] == "report1.json"


def test_export_csv():
    service = ReportExportService(FakeHistoryService(sample_reports()))

    exported = service.export_csv()

    assert "filename" in exported
    assert "report1.json" in exported
    assert "report2.json" in exported


def test_export_markdown():
    service = ReportExportService(FakeHistoryService(sample_reports()))

    exported = service.export_markdown()

    assert "| filename |" in exported
    assert "report1.json" in exported
    assert "report2.json" in exported


def test_export_single_report_json():
    service = ReportExportService(FakeHistoryService(sample_reports()))

    exported = service.export_report_json("report1.json")
    data = json.loads(exported)

    assert data["filename"] == "report1.json"


def test_export_single_report_csv():
    service = ReportExportService(FakeHistoryService(sample_reports()))

    exported = service.export_report_csv("report2.json")

    assert "report2.json" in exported
    assert "audit" in exported


def test_missing_report_returns_none():
    service = ReportExportService(FakeHistoryService(sample_reports()))

    assert service.export_report_json("missing.json") is None
    assert service.export_report_csv("missing.json") is None