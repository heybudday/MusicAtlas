from app.services.identity_audit_runner import IdentityAuditRunner


class FakeAuditService:
    def audit_artist(self, artist):
        return {
            "matched": True,
            "provider": "discogs",
            "confidence": 1.0,
        }


class FailingAuditService:
    def audit_artist(self, artist):
        raise RuntimeError("Provider timeout")


class MixedAuditService:
    def audit_artist(self, artist):
        if artist == "Broken Artist":
            raise RuntimeError("Lookup failed")

        return {
            "matched": True,
            "provider": "discogs",
            "confidence": 0.95,
        }


def test_audits_multiple_artists():
    runner = IdentityAuditRunner(FakeAuditService())

    reports = runner.audit_artists(
        [
            "Jeff Mills",
            "Robert Hood",
            "Underground Resistance",
        ]
    )

    assert len(reports) == 3

    assert reports[0]["query"] == "Jeff Mills"
    assert reports[1]["query"] == "Robert Hood"
    assert reports[2]["query"] == "Underground Resistance"

    assert all(report["matched"] for report in reports)


def test_failure_does_not_stop_batch():
    runner = IdentityAuditRunner(MixedAuditService())

    reports = runner.audit_artists(
        [
            "Jeff Mills",
            "Broken Artist",
            "Robert Hood",
        ]
    )

    assert len(reports) == 3

    assert reports[0]["matched"] is True

    assert reports[1]["matched"] is False
    assert reports[1]["query"] == "Broken Artist"
    assert reports[1]["error"] == "Lookup failed"

    assert reports[2]["matched"] is True


def test_all_failures_are_reported():
    runner = IdentityAuditRunner(FailingAuditService())

    reports = runner.audit_artists(
        [
            "Artist One",
            "Artist Two",
        ]
    )

    assert len(reports) == 2

    for report in reports:
        assert report["matched"] is False
        assert report["error"] == "Provider timeout"