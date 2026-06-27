from unittest.mock import Mock

import pytest

from app.identity_providers.musicbrainz import MusicBrainzProvider


def test_lookup_artist_matched():
    client = Mock()

    client.search_artist.return_value = {
        "id": "1234-abcd",
        "name": "Jeff Mills",
        "score": 100,
    }

    provider = MusicBrainzProvider(client=client)

    result = provider.lookup_artist("Jeff Mills")

    assert result == {
        "matched": True,
        "external_id": "1234-abcd",
        "url": "https://musicbrainz.org/artist/1234-abcd",
        "confidence": 1.0,
        "reason": "musicbrainz_artist_match",
    }


def test_lookup_artist_not_found():
    client = Mock()
    client.search_artist.return_value = None

    provider = MusicBrainzProvider(client=client)

    result = provider.lookup_artist("Unknown Artist")

    assert result == {
        "matched": False,
        "external_id": None,
        "url": None,
        "confidence": 0.0,
        "reason": "musicbrainz_artist_not_found",
    }


def test_lookup_label_matched():
    client = Mock()

    client.search_label.return_value = {
        "id": "abcd-5678",
        "name": "Warp Records",
        "score": 100,
    }

    provider = MusicBrainzProvider(client=client)

    result = provider.lookup_label("Warp Records")

    assert result == {
        "matched": True,
        "external_id": "abcd-5678",
        "url": "https://musicbrainz.org/label/abcd-5678",
        "confidence": 1.0,
        "reason": "musicbrainz_label_match",
    }


def test_lookup_label_not_found():
    client = Mock()
    client.search_label.return_value = None

    provider = MusicBrainzProvider(client=client)

    result = provider.lookup_label("Unknown Label")

    assert result == {
        "matched": False,
        "external_id": None,
        "url": None,
        "confidence": 0.0,
        "reason": "musicbrainz_label_not_found",
    }


def test_lookup_release_not_implemented():
    provider = MusicBrainzProvider(client=Mock())

    with pytest.raises(NotImplementedError):
        provider.lookup_release("Some Release")