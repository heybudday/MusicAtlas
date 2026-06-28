from app.services.report_delete_service import ReportDeleteService


class FakeArchive:
    def __init__(self, delete_result):
        self.delete_result = delete_result
        self.deleted_filename = None

    def delete_report(self, filename):
        self.deleted_filename = filename
        return self.delete_result


def test_delete_existing_report_returns_true():
    archive = FakeArchive(True)
    service = ReportDeleteService(archive)

    result = service.delete_report("identity_001.json")

    assert result is True


def test_delete_missing_report_returns_false():
    archive = FakeArchive(False)
    service = ReportDeleteService(archive)

    result = service.delete_report("missing.json")

    assert result is False


def test_correct_filename_is_passed_to_archive():
    archive = FakeArchive(True)
    service = ReportDeleteService(archive)

    service.delete_report("audit_report.json")

    assert archive.deleted_filename == "audit_report.json"


def test_returns_archive_result_unchanged():
    archive = FakeArchive(False)
    service = ReportDeleteService(archive)

    assert service.delete_report("example.json") is False

    archive = FakeArchive(True)
    service = ReportDeleteService(archive)

    assert service.delete_report("example.json") is True