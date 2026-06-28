import csv
import json

from app.services.identity_report_exporter import IdentityReportExporter


def sample_report():
    return {
        "summary": {
            "total": 2,
            "resolved": 1,
            "review": 1,
            "unresolved": 0,
        },
        "artists": [
            {
                "artist": "Jeff Mills",
                "status": "resolved",
                "confidence": 0.98,
                "provider": "discogs",
                "matched_name": "Jeff Mills",
                "matched_id": "123",
            },
            {
                "artist": "Robert Hood",
                "status": "review",
                "confidence": 0.74,
                "provider": "musicbrainz",
                "matched_name": "Robert Hood",
                "matched_id": "456",
            },
        ],
    }


def test_export_json_creates_file(tmp_path):
    exporter = IdentityReportExporter()

    output = tmp_path / "report.json"

    exporter.export_json(sample_report(), output)

    assert output.exists()

    with output.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["summary"] == sample_report()["summary"]


def test_export_json_overwrites_existing_file(tmp_path):
    exporter = IdentityReportExporter()

    output = tmp_path / "report.json"

    exporter.export_json({"summary": {"total": 1}}, output)
    exporter.export_json(sample_report(), output)

    with output.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["summary"] == sample_report()["summary"]


def test_export_csv_creates_file(tmp_path):
    exporter = IdentityReportExporter()

    output = tmp_path / "report.csv"

    exporter.export_csv(sample_report(), output)

    assert output.exists()

    with output.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    assert rows[0] == [
        "artist",
        "status",
        "confidence",
        "provider",
        "matched_name",
        "matched_id",
    ]

    assert len(rows) == 3


def test_export_csv_handles_missing_fields(tmp_path):
    exporter = IdentityReportExporter()

    report = {
        "artists": [
            {
                "artist": "Jeff Mills",
                "status": "resolved",
            }
        ]
    }

    output = tmp_path / "report.csv"

    exporter.export_csv(report, output)

    with output.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows[0]["artist"] == "Jeff Mills"
    assert rows[0]["status"] == "resolved"
    assert rows[0]["confidence"] == ""
    assert rows[0]["provider"] == ""
    assert rows[0]["matched_name"] == ""
    assert rows[0]["matched_id"] == ""


def test_export_creates_parent_directories(tmp_path):
    exporter = IdentityReportExporter()

    output = tmp_path / "nested" / "reports" / "report.json"

    exporter.export_json(sample_report(), output)

    assert output.exists()
    assert output.parent.exists()