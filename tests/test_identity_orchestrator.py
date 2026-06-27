from app.services import identity_orchestrator
from app.services.identity_orchestrator import IdentityOrchestrator


class FakeProvider:
    def lookup_artist(self, name):
        return {
            "matched": True,
            "external_id": "artist-123",
            "name": name,
        }

    def lookup_label(self, name):
        return {
            "matched": True,
            "external_id": "label-123",
            "name": name,
        }


def fake_create_provider(provider_name):
    assert provider_name == "fake"
    return FakeProvider()


def test_artist_orchestrator_calls_provider(monkeypatch):
    monkeypatch.setattr(
        identity_orchestrator,
        "create_provider",
        fake_create_provider,
    )

    orchestrator = IdentityOrchestrator()

    result = orchestrator.enrich_artist("Jeff Mills", ["fake"])

    assert result == [
        {
            "provider": "fake",
            "result": {
                "matched": True,
                "external_id": "artist-123",
                "name": "Jeff Mills",
            },
        }
    ]


def test_label_orchestrator_calls_provider(monkeypatch):
    monkeypatch.setattr(
        identity_orchestrator,
        "create_provider",
        fake_create_provider,
    )

    orchestrator = IdentityOrchestrator()

    result = orchestrator.enrich_label("Warp Records", ["fake"])

    assert result == [
        {
            "provider": "fake",
            "result": {
                "matched": True,
                "external_id": "label-123",
                "name": "Warp Records",
            },
        }
    ]


def test_lookup_artist_uses_existing_external_identity():
    class FakeRepository:
        def get(self, provider, entity_type, query):
            return None

        def upsert(self, data):
            pass

    class FakeExternalIdentityService:
        def find(self, entity_type, entity_key, service):
            return {
                "external_id": "12345",
                "url": "https://example.com/artist/12345",
            }

    class FakeProvider:
        called = False

        def lookup_artist(self, name):
            FakeProvider.called = True
            return {
                "provider": "fake",
                "entity_type": "artist",
                "query": name,
            }

    orchestrator = IdentityOrchestrator(
        providers={"fake": FakeProvider()},
        enrichment_repository=FakeRepository(),
    )

    orchestrator.external_identity_service = FakeExternalIdentityService()

    result = orchestrator.lookup_artist("The Beatles", "fake")

    assert result["external_id"] == "12345"
    assert FakeProvider.called is False