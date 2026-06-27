from app.services import identity_orchestrator
from app.services.identity_orchestrator import IdentityOrchestrator


class FakeProvider:
    artist_calls = 0
    label_calls = 0

    def lookup_artist(self, name):
        FakeProvider.artist_calls += 1
        return {
            "matched": True,
            "external_id": "artist-123",
            "name": name,
        }

    def lookup_label(self, name):
        FakeProvider.label_calls += 1
        return {
            "matched": True,
            "external_id": "label-123",
            "name": name,
        }


class FakeEnrichmentRepository:
    def __init__(self, cached=None):
        self.cached = cached
        self.upserted = []

    def get(self, provider, entity_type, query):
        return self.cached

    def upsert(self, data):
        self.upserted.append(data)


def fake_create_provider(provider_name):
    assert provider_name == "fake"
    return FakeProvider()


def test_artist_orchestrator_calls_provider(monkeypatch):
    FakeProvider.artist_calls = 0

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
    assert FakeProvider.artist_calls == 1


def test_label_orchestrator_calls_provider(monkeypatch):
    FakeProvider.label_calls = 0

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
    assert FakeProvider.label_calls == 1


def test_enrich_artist_uses_cached_enrichment():
    FakeProvider.artist_calls = 0

    cached = {
        "matched": True,
        "external_id": "cached-artist-123",
        "name": "Jeff Mills",
    }

    repository = FakeEnrichmentRepository(cached=cached)

    orchestrator = IdentityOrchestrator(
        providers={"fake": FakeProvider()},
        enrichment_repository=repository,
    )

    result = orchestrator.enrich_artist("Jeff Mills", ["fake"])

    assert result == [
        {
            "provider": "fake",
            "result": cached,
        }
    ]
    assert FakeProvider.artist_calls == 0
    assert repository.upserted == []


def test_enrich_artist_stores_uncached_enrichment():
    FakeProvider.artist_calls = 0

    repository = FakeEnrichmentRepository()

    orchestrator = IdentityOrchestrator(
        providers={"fake": FakeProvider()},
        enrichment_repository=repository,
    )

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
    assert FakeProvider.artist_calls == 1
    assert repository.upserted == [
        {
            "matched": True,
            "external_id": "artist-123",
            "name": "Jeff Mills",
        }
    ]


def test_enrich_label_uses_cached_enrichment():
    FakeProvider.label_calls = 0

    cached = {
        "matched": True,
        "external_id": "cached-label-123",
        "name": "Warp Records",
    }

    repository = FakeEnrichmentRepository(cached=cached)

    orchestrator = IdentityOrchestrator(
        providers={"fake": FakeProvider()},
        enrichment_repository=repository,
    )

    result = orchestrator.enrich_label("Warp Records", ["fake"])

    assert result == [
        {
            "provider": "fake",
            "result": cached,
        }
    ]
    assert FakeProvider.label_calls == 0
    assert repository.upserted == []


def test_enrich_label_stores_uncached_enrichment():
    FakeProvider.label_calls = 0

    repository = FakeEnrichmentRepository()

    orchestrator = IdentityOrchestrator(
        providers={"fake": FakeProvider()},
        enrichment_repository=repository,
    )

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
    assert FakeProvider.label_calls == 1
    assert repository.upserted == [
        {
            "matched": True,
            "external_id": "label-123",
            "name": "Warp Records",
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

    class FakeLookupProvider:
        called = False

        def lookup_artist(self, name):
            FakeLookupProvider.called = True
            return {
                "provider": "fake",
                "entity_type": "artist",
                "query": name,
            }

    orchestrator = IdentityOrchestrator(
        providers={"fake": FakeLookupProvider()},
        enrichment_repository=FakeRepository(),
    )

    orchestrator.external_identity_service = FakeExternalIdentityService()

    result = orchestrator.lookup_artist("The Beatles", "fake")

    assert result["external_id"] == "12345"
    assert FakeLookupProvider.called is False