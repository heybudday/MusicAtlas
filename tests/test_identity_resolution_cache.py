from app.services.identity_orchestrator import IdentityOrchestrator


class FakeRepository:
    def __init__(self):
        self.saved = None

    def find(self, entity_type, entity_key, service):
        return None

    def upsert(self, enrichment):
        self.saved = enrichment


class FakeProvider:
    def lookup_artist(self, name):
        return {
            "provider": "fake",
            "entity_type": "artist",
            "query": name,
        }


def test_orchestrator_saves_lookup():

    repo = FakeRepository()

    orchestrator = IdentityOrchestrator(
        providers={"fake": FakeProvider()},
        enrichment_repository=repo,
    )

    result = orchestrator.lookup_artist("Orbital", provider="fake")

    assert result["query"] == "Orbital"
    assert repo.saved is not None