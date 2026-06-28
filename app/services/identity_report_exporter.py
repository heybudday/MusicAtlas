from __future__ import annotations

import csv
import json
from pathlib import Path


class IdentityReportExporter:
    """
    Exports identity resolution reports to JSON or CSV.
    """

    CSV_COLUMNS = [
        "artist",
        "status",
        "confidence",
        "provider",
        "matched_name",
        "matched_id",
    ]

    def export_json(self, report, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return output_path

    def export_csv(self, report, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        artists = report.get("artists", [])

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_COLUMNS)
            writer.writeheader()

            for artist in artists:
                writer.writerow(
                    {
                        "artist": artist.get("artist", ""),
                        "status": artist.get("status", ""),
                        "confidence": artist.get("confidence", ""),
                        "provider": artist.get("provider", ""),
                        "matched_name": artist.get("matched_name", ""),
                        "matched_id": artist.get("matched_id", ""),
                    }
                )

        return output_path