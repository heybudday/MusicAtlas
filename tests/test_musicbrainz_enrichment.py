from app.enrichment.musicbrainz import MusicBrainzEnrichmentProvider


class FakeMusicBrainzClient:

    def get_artist(self, external_id: str):
        return {
            "id": external_id,
            "name": "Test Artist",
            "type": "Person",
        }


def test_musicbrainz_artist_enrichment():

    provider = MusicBrainzEnrichmentProvider(client=FakeMusicBrainzClient())

    result = provider.enrich_artist("123")

    assert result.success is True
    assert result.provider == "musicbrainz"
    assert result.data["id"] == "123"
    assert result.data["name"] == "Test Artist"
    assert result.errors == []