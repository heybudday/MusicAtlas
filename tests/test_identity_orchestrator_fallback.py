from app.services.identity_orchestrator import IdentityOrchestrator


class MatchingProvider:
    def lookup_artist(self, name):
        return {
            "matched": True,
            "name": name,
        }

    def lookup_label(self, name):
        return {
            "matched": True,
            "name": name,
        }


class NoMatchProvider:
    def lookup_artist(self, name):
        return {
            "matched": False,
        }

    def lookup_label(self, name):
        return {
            "matched": False,
        }


def test_resolve_artist_prefers_matching_provider():
    orchestrator = IdentityOrchestrator(
        providers={
            "nomatch": NoMatchProvider(),
            "matching": MatchingProvider(),
        }
    )

    result = orchestrator.resolve_artist(
        "Jeff Mills",
        ["nomatch", "matching"],
    )

    assert result["provider"] == "matching"
    assert result["result"]["matched"] is True


def test_resolve_label_prefers_matching_provider():
    orchestrator = IdentityOrchestrator(
        providers={
            "nomatch": NoMatchProvider(),
            "matching": MatchingProvider(),
        }
    )

    result = orchestrator.resolve_label(
        "Axis",
        ["nomatch", "matching"],
    )

    assert result["provider"] == "matching"
    assert result["result"]["matched"] is True


def test_resolve_artist_returns_unmatched_result_when_no_provider_matches():
    orchestrator = IdentityOrchestrator(
        providers={
            "nomatch": NoMatchProvider(),
        }
    )

    result = orchestrator.resolve_artist(
        "Jeff Mills",
        ["nomatch"],
    )

    assert result["provider"] == "nomatch"
    assert result["confidence"] == 0.0
    assert result["result"]["matched"] is False


def test_resolve_label_returns_unmatched_result_when_no_provider_matches():
    orchestrator = IdentityOrchestrator(
        providers={
            "nomatch": NoMatchProvider(),
        }
    )

    result = orchestrator.resolve_label(
        "Axis",
        ["nomatch"],
    )

    assert result["provider"] == "nomatch"
    assert result["confidence"] == 0.0
    assert result["result"]["matched"] is False