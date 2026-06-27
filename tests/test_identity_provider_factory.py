from app.identity_providers.discogs import DiscogsProvider
from app.identity_providers.factory import create_provider
from app.identity_providers.musicbrainz import MusicBrainzProvider


def test_create_discogs():
    provider = create_provider("discogs")
    assert isinstance(provider, DiscogsProvider)


def test_create_musicbrainz():
    provider = create_provider("musicbrainz")
    assert isinstance(provider, MusicBrainzProvider)


def test_unknown_provider():
    try:
        create_provider("foobar")
        assert False
    except ValueError:
        pass