import pytest

from app.services.report_archive_loader import ReportArchiveLoader


def test_load_existing_archived_report(tmp_path):
    archive = tmp_path / "reports"
    archive.mkdir()

    report = archive / "identity-report.txt"
    report.write_text("Identity report contents")

    loader = ReportArchiveLoader(archive)

    assert loader.load("identity-report.txt") == "Identity report contents"


def test_load_multiple_archived_reports(tmp_path):
    archive = tmp_path / "reports"
    archive.mkdir()

    (archive / "first.txt").write_text("First report")
    (archive / "second.txt").write_text("Second report")

    loader = ReportArchiveLoader(archive)

    assert loader.load("first.txt") == "First report"
    assert loader.load("second.txt") == "Second report"


def test_load_missing_archived_report_raises_clear_error(tmp_path):
    loader = ReportArchiveLoader(tmp_path)

    with pytest.raises(FileNotFoundError, match="Archived report not found"):
        loader.load("missing.txt")


def test_load_empty_archived_report(tmp_path):
    archive = tmp_path / "reports"
    archive.mkdir()

    (archive / "empty.txt").write_text("")

    loader = ReportArchiveLoader(archive)

    assert loader.load("empty.txt") == ""


def test_preserves_report_contents_exactly(tmp_path):
    archive = tmp_path / "reports"
    archive.mkdir()

    contents = "Line one\nLine two\n\nFinal line\n"
    (archive / "exact.txt").write_text(contents)

    loader = ReportArchiveLoader(archive)

    assert loader.load("exact.txt") == contents