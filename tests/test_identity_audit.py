from app.services.identity_audit import IdentityAudit


class FakeOrchestrator:
    def enrich_artist(self, name):
        return {
            "matched": True,
            "provider": "discogs",
            "confidence": 1.0,
            "reason": "exact_name_match",
            "result": {
                "name": name,
                "external_id": "12345",
            },
        }


def test_identity_audit_runs_for_artist():
    audit = IdentityAudit(orchestrator=FakeOrchestrator())

    result = audit.audit_artist("Jeff Mills")

    assert result["entity_type"] == "artist"
    assert result["query"] == "Jeff Mills"
    assert result["matched"] is True
    assert result["confidence"] == 1.0


def test_identity_audit_returns_confidence_decision():
    class FakeOrchestrator:
        def enrich_artist(self, name):
            return {
                "matched": True,
                "provider": "musicbrainz",
                "confidence": 0.82,
                "reason": "partial_name_match",
                "result": {
                    "name": name,
                },
            }

    audit = IdentityAudit(orchestrator=FakeOrchestrator())

    result = audit.audit_artist("Jeff Mills")

    assert result["matched"] is True
    assert result["provider"] == "musicbrainz"
    assert result["confidence"] == 0.82
    assert result["reason"] == "partial_name_match"


def test_identity_audit_flags_review_when_ambiguous():
    class FakeOrchestrator:
        def enrich_artist(self, name):
            return {
                "matched": True,
                "provider": "discogs",
                "confidence": 0.61,
                "reason": "partial_name_match",
                "review_recommended": True,
                "result": {
                    "name": "Jeff",
                },
            }

    audit = IdentityAudit(orchestrator=FakeOrchestrator())

    result = audit.audit_artist("Jeff Mills")

    assert result["matched"] is True
    assert result["review_recommended"] is True