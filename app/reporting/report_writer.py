from __future__ import annotations

from pathlib import Path


class ReportWriter:
    """
    Writes report files to an output directory.
    """

    def __init__(self, output_directory="reports"):
        self.output_directory = Path(output_directory)

    def write(self, filename: str, content: str):
        self.output_directory.mkdir(parents=True, exist_ok=True)

        path = self.output_directory / filename
        path.write_text(content, encoding="utf-8")

        return path