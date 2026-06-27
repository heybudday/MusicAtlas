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

    assert results == [
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "external_id": "1234-abcd",
                "url": "https://musicbrainz.org/artist/1234-abcd",
                "confidence": 1.0,
                "reason": "musicbrainz_artist_match",
            },
        }
    ]

    external_identity_service.upsert.assert_called_once_with(
        entity_type="artist",
        entity_key="artist_unresolved:jeff-mills",
        service="musicbrainz",
        external_id="1234-abcd",
        external_url="https://musicbrainz.org/artist/1234-abcd",
        confidence=1.0,
        source="identity_orchestrator",
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

    assert results == [
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "external_id": "abcd-5678",
                "url": "https://musicbrainz.org/label/abcd-5678",
                "confidence": 1.0,
                "reason": "musicbrainz_label_match",
            },
        }
    ]

    external_identity_service.upsert.assert_called_once_with(
        entity_type="label",
        entity_key="label_unresolved:warp-records",
        service="musicbrainz",
        external_id="abcd-5678",
        external_url="https://musicbrainz.org/label/abcd-5678",
        confidence=1.0,
        source="identity_orchestrator",
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

    orchestrator.resolve_artist(
        artist_key="artist_unresolved:unknown",
        artist_name="Unknown Artist",
        providers=["musicbrainz"],
    )

    external_identity_service.upsert.assert_not_called()