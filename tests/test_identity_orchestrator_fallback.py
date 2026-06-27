from app.services.identity_orchestrator import IdentityOrchestrator


class MatchingProvider:
    def lookup_artist(self, name):
        return {
            "matched": True,
            "provider": "matching",
            "entity_type": "artist",
            "query": name,
            "name": name,
        }

    def lookup_label(self, name):
        return {
            "matched": True,
            "provider": "matching",
            "entity_type": "label",
            "query": name,
            "name": name,
        }


class NoMatchProvider:
    def lookup_artist(self, name):
        return {
            "matched": False,
            "provider": "nomatch",
            "entity_type": "artist",
            "query": name,
        }

    def lookup_label(self, name):
        return {
            "matched": False,
            "provider": "nomatch",
            "entity_type": "label",
            "query": name,
        }


class FailingProvider:
    def lookup_artist(self, name):
        raise RuntimeError("provider unavailable")

    def lookup_label(self, name):
        raise RuntimeError("provider unavailable")


class FakeEnrichmentRepository:
    def __init__(self):
        self.records = []

    def get(self, provider, entity_type, query):
        return None

    def upsert(self, result):
        self.records.append(result)


def test_artist_lookup_falls_back_after_no_match():
    orchestrator = IdentityOrchestrator(
        providers={
            "nomatch": NoMatchProvider(),
            "matching": MatchingProvider(),
        }
    )

    result = orchestrator.lookup_artist_with_fallback(
        "Jeff Mills",
        ["nomatch", "matching"],
    )

    assert result["matched"] is True
    assert result["provider"] == "matching"


def test_artist_lookup_falls_back_after_provider_error():
    orchestrator = IdentityOrchestrator(
        providers={
            "failing": FailingProvider(),
            "matching": MatchingProvider(),
        }
    )

    result = orchestrator.lookup_artist_with_fallback(
        "Jeff Mills",
        ["failing", "matching"],
    )

    assert result["matched"] is True
    assert result["provider"] == "matching"


def test_label_lookup_falls_back_after_no_match():
    orchestrator = IdentityOrchestrator(
        providers={
            "nomatch": NoMatchProvider(),
            "matching": MatchingProvider(),
        }
    )

    result = orchestrator.lookup_label_with_fallback(
        "Axis",
        ["nomatch", "matching"],
    )

    assert result["matched"] is True
    assert result["provider"] == "matching"


def test_successful_fallback_result_is_cached():
    repository = FakeEnrichmentRepository()

    orchestrator = IdentityOrchestrator(
        providers={
            "nomatch": NoMatchProvider(),
            "matching": MatchingProvider(),
        },
        enrichment_repository=repository,
    )

    result = orchestrator.lookup_artist_with_fallback(
        "Jeff Mills",
        ["nomatch", "matching"],
    )

    assert result["matched"] is True
    assert repository.records == [result]