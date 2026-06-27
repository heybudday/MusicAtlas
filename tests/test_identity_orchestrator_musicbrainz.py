from unittest.mock import Mock, patch

from app.services.identity_orchestrator import IdentityOrchestrator


@patch("app.services.identity_orchestrator.create_provider")
def test_enrich_artist_with_musicbrainz(mock_create_provider):
    provider = Mock()

    provider.lookup_artist.return_value = {
        "matched": True,
        "name": "Jeff Mills",
        "external_id": "1234-abcd",
        "url": "https://musicbrainz.org/artist/1234-abcd",
        "confidence": 1.0,
        "reason": "musicbrainz_artist_match",
    }

    mock_create_provider.return_value = provider

    orchestrator = IdentityOrchestrator()

    results = orchestrator.enrich_artist(
        "Jeff Mills",
        providers=["musicbrainz"],
    )

    assert results["results"] == [
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "name": "Jeff Mills",
                "external_id": "1234-abcd",
                "url": "https://musicbrainz.org/artist/1234-abcd",
                "confidence": 1.0,
                "reason": "musicbrainz_artist_match",
            },
        }
    ]

    assert results["best_match"]["provider"] == "musicbrainz"


@patch("app.services.identity_orchestrator.create_provider")
def test_enrich_label_with_musicbrainz(mock_create_provider):
    provider = Mock()

    provider.lookup_label.return_value = {
        "matched": True,
        "name": "Warp Records",
        "external_id": "abcd-5678",
        "url": "https://musicbrainz.org/label/abcd-5678",
        "confidence": 1.0,
        "reason": "musicbrainz_label_match",
    }

    mock_create_provider.return_value = provider

    orchestrator = IdentityOrchestrator()

    results = orchestrator.enrich_label(
        "Warp Records",
        providers=["musicbrainz"],
    )

    assert results["results"] == [
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "name": "Warp Records",
                "external_id": "abcd-5678",
                "url": "https://musicbrainz.org/label/abcd-5678",
                "confidence": 1.0,
                "reason": "musicbrainz_label_match",
            },
        }
    ]

    assert results["best_match"]["provider"] == "musicbrainz"