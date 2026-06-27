from app.identity_providers.discogs import DiscogsProvider
from app.identity_providers.musicbrainz import MusicBrainzProvider
from app.identity_providers.spotify import SpotifyProvider


def test_providers_can_be_constructed():
    assert isinstance(DiscogsProvider(), DiscogsProvider)
    assert isinstance(SpotifyProvider(), SpotifyProvider)
    assert isinstance(MusicBrainzProvider(), MusicBrainzProvider)