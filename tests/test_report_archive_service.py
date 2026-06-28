from __future__ import annotations

from datetime import datetime

import pytest

from app.services.report_archive_service import ReportArchiveService


def test_archive_report_copies_file_to_dated_report_type_directory(tmp_path):
    source = tmp_path / "identity_report.csv"
    source.write_text("artist,status\nJeff Mills,resolved\n")

    archive_root = tmp_path / "archive"
    service = ReportArchiveService(archive_root)

    archived_path = service.archive_report(
        source,
        "identity",
        timestamp=datetime(2026, 6, 27, 14, 30, 5),
    )

    assert archived_path == (
        archive_root / "identity" / "2026-06-27" / "identity_report_143005.csv"
    )
    assert archived_path.read_text() == "artist,status\nJeff Mills,resolved\n"


def test_archive_report_preserves_source_file(tmp_path):
    source = tmp_path / "summary.txt"
    source.write_text("summary contents")

    service = ReportArchiveService(tmp_path / "archive")

    service.archive_report(
        source,
        "summary",
        timestamp=datetime(2026, 6, 27, 9, 0, 0),
    )

    assert source.exists()
    assert source.read_text() == "summary contents"


def test_archive_report_raises_for_missing_source(tmp_path):
    service = ReportArchiveService(tmp_path / "archive")

    with pytest.raises(FileNotFoundError):
        service.archive_report(
            tmp_path / "missing.csv",
            "identity",
            timestamp=datetime(2026, 6, 27, 14, 30, 5),
        )