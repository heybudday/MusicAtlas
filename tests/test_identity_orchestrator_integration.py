from unittest.mock import Mock, patch

from app.services.identity_orchestrator import IdentityOrchestrator


@patch("app.services.identity_orchestrator.ExternalIdentityService")
@patch("app.services.identity_orchestrator.create_provider")
def test_resolve_artist_persists_matched_identity(
    mock_create_provider,
    mock_external_identity_service,
):
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

    external_identity_service = Mock()
    mock_external_identity_service.return_value = external_identity_service

    session = Mock()
    orchestrator = IdentityOrchestrator(session=session)

    results = orchestrator.resolve_artist(
        artist_key="artist_unresolved:jeff-mills",
        artist_name="Jeff Mills",
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

    external_identity_service.get_or_create.assert_called_once_with(
        {
            "source_key": "artist_unresolved:jeff-mills",
            "entity_type": "artist",
            "matched": True,
            "name": "Jeff Mills",
            "external_id": "1234-abcd",
            "url": "https://musicbrainz.org/artist/1234-abcd",
            "confidence": 1.0,
            "reason": "musicbrainz_artist_match",
        }
    )


@patch("app.services.identity_orchestrator.ExternalIdentityService")
@patch("app.services.identity_orchestrator.create_provider")
def test_resolve_label_persists_matched_identity(
    mock_create_provider,
    mock_external_identity_service,
):
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

    external_identity_service = Mock()
    mock_external_identity_service.return_value = external_identity_service

    session = Mock()
    orchestrator = IdentityOrchestrator(session=session)

    results = orchestrator.resolve_label(
        label_key="label_unresolved:warp-records",
        label_name="Warp Records",
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

    external_identity_service.get_or_create.assert_called_once_with(
        {
            "source_key": "label_unresolved:warp-records",
            "entity_type": "label",
            "matched": True,
            "name": "Warp Records",
            "external_id": "abcd-5678",
            "url": "https://musicbrainz.org/label/abcd-5678",
            "confidence": 1.0,
            "reason": "musicbrainz_label_match",
        }
    )


@patch("app.services.identity_orchestrator.ExternalIdentityService")
@patch("app.services.identity_orchestrator.create_provider")
def test_resolve_artist_does_not_persist_unmatched_identity(
    mock_create_provider,
    mock_external_identity_service,
):
    provider = Mock()
    provider.lookup_artist.return_value = {
        "matched": False,
        "name": "Unknown Artist",
        "external_id": None,
        "url": None,
        "confidence": 0.0,
        "reason": "musicbrainz_artist_not_found",
    }

    mock_create_provider.return_value = provider

    external_identity_service = Mock()
    mock_external_identity_service.return_value = external_identity_service

    session = Mock()
    orchestrator = IdentityOrchestrator(session=session)

    results = orchestrator.resolve_artist(
        artist_key="artist_unresolved:unknown",
        artist_name="Unknown Artist",
        providers=["musicbrainz"],
    )

    assert results["best_match"] is None
    external_identity_service.get_or_create.assert_not_called()