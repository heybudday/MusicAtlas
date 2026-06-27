from app.services.identity_orchestrator import IdentityOrchestrator


class FakeProvider:
    def lookup_artist(self, name):
        return {
            "matched": True,
            "name": name,
            "external_id": "123",
            "confidence": 0.86,
        }


class FakeConfidenceScorer:
    def select_best(self, query, results, threshold=0.75):
        return {
            "provider": "discogs",
            "result": {
                "matched": True,
                "name": "Jeff Mills",
                "external_id": "123",
                "confidence": 0.86,
            },
            "confidence": 0.86,
            "confidence_margin": 0.03,
            "review_recommended": True,
            "reason": "ambiguous_identity_match",
        }


class FakeExternalIdentityService:
    def __init__(self):
        self.persisted = []

    def upsert_artist_identity(self, artist, best_match):
        self.persisted.append((artist, best_match))


def test_orchestrator_surfaces_review_recommendation_in_decision_summary():
    orchestrator = IdentityOrchestrator(
        providers={"discogs": FakeProvider()},
        confidence_scorer=FakeConfidenceScorer(),
    )

    result = orchestrator.resolve_artist("Jeff Mills", ["discogs"])

    assert result["decision"]["confidence_margin"] == 0.03
    assert result["decision"]["review_recommended"] is True
    assert result["decision"]["reason"] == "ambiguous_identity_match"


def test_orchestrator_persistence_threshold_still_applies():
    external_identity_service = FakeExternalIdentityService()

    orchestrator = IdentityOrchestrator(
        providers={"discogs": FakeProvider()},
        confidence_scorer=FakeConfidenceScorer(),
    )
    orchestrator.external_identity_service = external_identity_service

    result = orchestrator.resolve_artist("Jeff Mills", ["discogs"])

    assert result["decision"]["review_recommended"] is True

    # Confidence (0.86) is below the persistence threshold (0.90),
    # so nothing should be persisted.
    assert external_identity_service.persisted == []