from __future__ import annotations

from datetime import datetime
from pathlib import Path
from shutil import copyfile


class ReportArchiveService:
    """
    Archives generated report files into a dated archive directory.
    """

    def __init__(self, archive_root: str | Path = "reports/archive"):
        self.archive_root = Path(archive_root)

    def archive_report(
        self,
        source_path: str | Path,
        report_type: str,
        timestamp: datetime | None = None,
    ) -> Path:
        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(f"Report file not found: {source}")

        created_at = timestamp or datetime.now()
        archive_dir = self.archive_root / report_type / created_at.strftime("%Y-%m-%d")
        archive_dir.mkdir(parents=True, exist_ok=True)

        archived_path = archive_dir / self._archive_filename(source, created_at)
        copyfile(source, archived_path)

        return archived_path

    def _archive_filename(self, source: Path, created_at: datetime) -> str:
        timestamp = created_at.strftime("%H%M%S")
        return f"{source.stem}_{timestamp}{source.suffix}"