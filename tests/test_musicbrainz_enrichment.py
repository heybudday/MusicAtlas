from app.enrichment.musicbrainz import MusicBrainzEnrichmentProvider


def test_musicbrainz_stub():

    provider = MusicBrainzEnrichmentProvider()

    result = provider.enrich_artist("123")

    assert result.success is True
    assert result.provider == "musicbrainz"