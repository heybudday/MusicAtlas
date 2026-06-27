from app.services.identity_orchestrator import IdentityOrchestrator


class FakeProvider:
    def __init__(self):
        self.calls = 0

    def lookup_artist(self, artist):
        self.calls += 1
        return {
            "provider": "fake",
            "entity_type": "artist",
            "query": artist,
        }


class FakeRepository:
    def __init__(self):
        self.data = {}

    def get(self, provider, entity_type, query):
        return self.data.get((provider, entity_type, query))

    def upsert(self, result):
        key = (
            result["provider"],
            result["entity_type"],
            result["query"],
        )
        self.data[key] = result


def test_lookup_artist_uses_cache():
    provider = FakeProvider()
    repository = FakeRepository()

    orchestrator = IdentityOrchestrator(
        providers={"fake": provider},
        enrichment_repository=repository,
    )

    first = orchestrator.lookup_artist("Jeff Mills", "fake")
    second = orchestrator.lookup_artist("Jeff Mills", "fake")

    assert first == second
    assert provider.calls == 1