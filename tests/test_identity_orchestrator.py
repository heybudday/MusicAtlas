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

    assert "results" in result
    assert "best_match" in result

    assert result["results"] == [
        {
            "provider": "fake",
            "result": {
                "matched": True,
                "external_id": "artist-123",
                "name": "Jeff Mills",
            },
        }
    ]

    assert result["best_match"]["provider"] == "fake"


def test_label_orchestrator_calls_provider(monkeypatch):
    monkeypatch.setattr(
        identity_orchestrator,
        "create_provider",
        fake_create_provider,
    )

    orchestrator = IdentityOrchestrator()

    result = orchestrator.enrich_label("Axis", ["fake"])

    assert "results" in result
    assert "best_match" in result

    assert result["results"] == [
        {
            "provider": "fake",
            "result": {
                "matched": True,
                "external_id": "label-123",
                "name": "Axis",
            },
        }
    ]

    assert result["best_match"]["provider"] == "fake"


def test_enrich_artist_returns_best_match():
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

    result = orchestrator.enrich_artist(
        "Jeff Mills",
        ["low", "high"],
    )

    assert "results" in result
    assert "best_match" in result
    assert result["best_match"]["provider"] == "high"
    assert result["best_match"]["result"]["name"] == "Jeff Mills"


def test_enrich_artist_best_match_is_none_when_below_threshold():
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

    result = orchestrator.enrich_artist(
        "Jeff Mills",
        ["weak"],
        confidence_threshold=0.95,
    )

    assert result["best_match"] is None