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

    result = orchestrator.enrich_label("Axis", ["fake"])

    assert result == [
        {
            "provider": "fake",
            "result": {
                "matched": True,
                "external_id": "label-123",
                "name": "Axis",
            },
        }
    ]


def test_resolve_artist_returns_best_match():
    class LowConfidenceProvider:
        def lookup_artist(self, name):
            return {
                "matched": True,
                "name": "Jeff",
            }

    class HighConfidenceProvider:
        def lookup_artist(self, name):
            return {
                "matched": True,
                "name": "Jeff Mills",
            }

    orchestrator = IdentityOrchestrator(
        providers={
            "low": LowConfidenceProvider(),
            "high": HighConfidenceProvider(),
        }
    )

    result = orchestrator.resolve_artist(
        "Jeff Mills",
        ["low", "high"],
    )

    assert result["provider"] == "high"
    assert result["result"]["name"] == "Jeff Mills"


def test_resolve_artist_returns_low_confidence_best_match():
    class WeakProvider:
        def lookup_artist(self, name):
            return {
                "matched": True,
                "name": "Jeff",
            }

    orchestrator = IdentityOrchestrator(
        providers={
            "weak": WeakProvider(),
        }
    )

    result = orchestrator.resolve_artist(
        "Jeff Mills",
        ["weak"],
    )

    assert result["provider"] == "weak"
    assert (
        result["confidence"]
        < IdentityOrchestrator.DEFAULT_PERSIST_THRESHOLD
    )