from __future__ import annotations

import csv
import json

from app.services.identity_audit_exporter import IdentityAuditExporter


def test_export_json_includes_summary_and_results(tmp_path):
    summary = {
        "processed": 2,
        "success": 1,
        "review": 1,
        "failed": 0,
    }

    results = [
        {
            "query": "Aphex Twin",
            "status": "matched",
            "provider": "discogs",
        },
        {
            "query": "Unknown Artist",
            "status": "review",
            "provider": "musicbrainz",
        },
    ]

    exporter = IdentityAuditExporter(tmp_path)
    exported_files = exporter.export(summary, results, "json")

    assert len(exported_files) == 1

    path = exported_files[0]

    assert path.exists()
    assert path.suffix == ".json"
    assert path.name.startswith("identity_audit_")

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["summary"] == summary
    assert payload["results"] == results


def test_export_csv_includes_results_and_summary(tmp_path):
    summary = {
        "processed": 1,
        "success": 1,
        "review": 0,
        "failed": 0,
    }

    results = [
        {
            "query": "Boards Of Canada",
            "status": "matched",
            "provider": "discogs",
        }
    ]

    exporter = IdentityAuditExporter(tmp_path)
    exported_files = exporter.export(summary, results, "csv")

    assert len(exported_files) == 1

    path = exported_files[0]

    assert path.exists()
    assert path.suffix == ".csv"
    assert path.name.startswith("identity_audit_")

    with path.open(encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["query"] == "Boards Of Canada"
    assert rows[0]["status"] == "matched"
    assert rows[0]["provider"] == "discogs"

    summary_rows = [row for row in rows if row["section"] == "summary"]

    assert summary_rows


def test_export_both_creates_json_and_csv(tmp_path):
    exporter = IdentityAuditExporter(tmp_path)

    exported_files = exporter.export(
        summary={"processed": 0},
        results=[],
        export_format="both",
    )

    suffixes = sorted(path.suffix for path in exported_files)

    assert suffixes == [".csv", ".json"]