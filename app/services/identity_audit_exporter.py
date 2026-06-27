from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


class IdentityAuditExporter:
    """
    Exports identity audit summaries and detailed results.
    """

    DEFAULT_OUTPUT_DIR = "reports"

    def __init__(self, output_dir: str | Path | None = None):
        self.output_dir = Path(output_dir or self.DEFAULT_OUTPUT_DIR)

    def export(self, summary, results=None, export_format="json"):
        if export_format not in {"json", "csv", "both"}:
            raise ValueError("export_format must be json, csv, or both")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        exported_files = []

        if export_format in {"json", "both"}:
            exported_files.append(self.export_json(summary, results))

        if export_format in {"csv", "both"}:
            exported_files.append(self.export_csv(summary, results))

        return exported_files

    def export_json(self, summary, results=None):
        path = self._path("json")

        payload = {
            "summary": summary,
            "results": results or [],
        }

        path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )

        return path

    def export_csv(self, summary, results=None):
        path = self._path("csv")

        rows = results or []

        fieldnames = self._fieldnames(rows)

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in rows:
                writer.writerow(self._flatten_row(row, fieldnames))

            writer.writerow({})
            writer.writerow({"section": "summary"})

            for key, value in summary.items():
                writer.writerow(
                    {
                        "section": "summary",
                        "key": key,
                        "value": json.dumps(value, sort_keys=True),
                    }
                )

        return path

    def _path(self, extension):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self.output_dir / f"identity_audit_{timestamp}.{extension}"

    def _fieldnames(self, rows):
        fields = {"section", "key", "value"}

        for row in rows:
            fields.update(row.keys())

        return sorted(fields)

    def _flatten_row(self, row, fieldnames):
        flattened = {}

        for field in fieldnames:
            value = row.get(field, "")

            if isinstance(value, (dict, list)):
                value = json.dumps(value, sort_keys=True)

            flattened[field] = value

        return flattened