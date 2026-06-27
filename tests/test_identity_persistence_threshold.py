from app.services.identity_orchestrator import IdentityOrchestrator


class FakeConfidenceScorer:
    def __init__(self, best_match):
        self.best_match = best_match

    def select_best(self, query, results, threshold=0.75):
        return self.best_match


class FakeExternalIdentityService:
    def __init__(self):
        self.artist_calls = []
        self.label_calls = []

    def upsert_artist_identity(self, artist, best_match):
        self.artist_calls.append((artist, best_match))

    def upsert_label_identity(self, label, best_match):
        self.label_calls.append((label, best_match))


def make_orchestrator(best_match):
    orchestrator = IdentityOrchestrator(
        confidence_scorer=FakeConfidenceScorer(best_match),
    )

    orchestrator.external_identity_service = FakeExternalIdentityService()
    orchestrator.enrich_artist = lambda artist, providers=None: []
    orchestrator.enrich_label = lambda label, providers=None: []

    return orchestrator


def test_persists_artist_identity_at_full_confidence():
    best_match = {
        "provider": "discogs",
        "confidence": 1.0,
        "result": {
            "matched": True,
        },
    }

    orchestrator = make_orchestrator(best_match)

    orchestrator.resolve_artist("Jeff Mills")

    assert len(
        orchestrator.external_identity_service.artist_calls
    ) == 1


def test_persists_artist_identity_at_threshold():
    best_match = {
        "provider": "discogs",
        "confidence": IdentityOrchestrator.DEFAULT_PERSIST_THRESHOLD,
        "result": {
            "matched": True,
        },
    }

    orchestrator = make_orchestrator(best_match)

    orchestrator.resolve_artist("Jeff Mills")

    assert len(
        orchestrator.external_identity_service.artist_calls
    ) == 1


def test_does_not_persist_artist_identity_below_threshold():
    best_match = {
        "provider": "discogs",
        "confidence": (
            IdentityOrchestrator.DEFAULT_PERSIST_THRESHOLD
            - 0.01
        ),
        "result": {
            "matched": True,
        },
    }

    orchestrator = make_orchestrator(best_match)

    orchestrator.resolve_artist("Jeff Mills")

    assert (
        orchestrator.external_identity_service.artist_calls
        == []
    )


def test_does_not_persist_artist_identity_without_best_match():
    orchestrator = make_orchestrator(None)

    orchestrator.resolve_artist("Jeff Mills")

    assert (
        orchestrator.external_identity_service.artist_calls
        == []
    )