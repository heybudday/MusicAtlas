from app.clients.musicbrainz import MusicBrainzClient


def test_client_exists():
    client = MusicBrainzClient()
    assert client is not None