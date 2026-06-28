from datetime import datetime
from time import sleep

from app.services.report_archive_service import ReportArchiveService


def test_archive_creates_record():
    service = ReportArchiveService()

    entry = service.archive(
        report_type="identity",
        filename="identity.csv",
        path="/reports/identity.csv",
        record_count=123,
    )

    assert entry["id"] == 1
    assert entry["report_type"] == "identity"
    assert entry["filename"] == "identity.csv"
    assert entry["path"] == "/reports/identity.csv"
    assert entry["record_count"] == 123


def test_archive_assigns_timestamp():
    service = ReportArchiveService()

    entry = service.archive(
        report_type="identity",
        filename="identity.csv",
        path="/reports/identity.csv",
        record_count=10,
    )

    assert isinstance(entry["generated_at"], datetime)


def test_list_returns_newest_first():
    service = ReportArchiveService()

    first = service.archive(
        report_type="identity",
        filename="first.csv",
        path="/reports/first.csv",
        record_count=1,
    )

    sleep(0.01)

    second = service.archive(
        report_type="identity",
        filename="second.csv",
        path="/reports/second.csv",
        record_count=2,
    )

    reports = service.list_reports()

    assert reports[0]["id"] == second["id"]
    assert reports[1]["id"] == first["id"]


def test_get_returns_correct_report():
    service = ReportArchiveService()

    entry = service.archive(
        report_type="identity",
        filename="identity.csv",
        path="/reports/identity.csv",
        record_count=5,
    )

    report = service.get(entry["id"])

    assert report == entry


def test_get_by_filename_returns_correct_report():
    service = ReportArchiveService()

    entry = service.archive(
        report_type="identity",
        filename="identity.csv",
        path="/reports/identity.csv",
        record_count=5,
    )

    report = service.get_by_filename("identity.csv")

    assert report == entry


def test_unknown_report_returns_none():
    service = ReportArchiveService()

    assert service.get(999) is None
    assert service.get_by_filename("missing.csv") is None


def test_empty_archive_returns_empty_list():
    service = ReportArchiveService()

    assert service.list_reports() == []