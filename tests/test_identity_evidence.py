from app.services.identity_evidence import IdentityEvidenceCollector


def test_collects_populated_evidence_fields():
    collector = IdentityEvidenceCollector()

    result = {
        "website": "https://jeffmills.com",
        "spotify": "https://open.spotify.com/artist/example",
    }

    evidence = collector.collect(
        provider="discogs",
        result=result,
    )

    assert evidence["website"] == "https://jeffmills.com"
    assert evidence["spotify"] == "https://open.spotify.com/artist/example"


def test_missing_evidence_fields_are_present_and_none():
    collector = IdentityEvidenceCollector()

    evidence = collector.collect(
        provider="discogs",
        result={},
    )

    expected_fields = [
        "website",
        "spotify",
        "discogs",
        "musicbrainz",
        "bandcamp",
        "soundcloud",
        "facebook",
        "instagram",
        "twitter",
        "youtube",
        "tiktok",
    ]

    for field in expected_fields:
        assert field in evidence
        assert evidence[field] is None


def test_sources_contains_entries_for_populated_fields():
    collector = IdentityEvidenceCollector()

    result = {
        "website": "https://jeffmills.com",
        "spotify": "https://open.spotify.com/artist/example",
    }

    evidence = collector.collect(
        provider="discogs",
        result=result,
    )

    assert {
        "field": "website",
        "provider": "discogs",
        "confidence": 1.0,
    } in evidence["sources"]

    assert {
        "field": "spotify",
        "provider": "discogs",
        "confidence": 1.0,
    } in evidence["sources"]


def test_provider_name_is_copied_into_every_source_record():
    collector = IdentityEvidenceCollector()

    result = {
        "website": "https://jeffmills.com",
        "bandcamp": "https://jeffmills.bandcamp.com",
        "soundcloud": "https://soundcloud.com/jeffmills",
    }

    evidence = collector.collect(
        provider="musicbrainz",
        result=result,
    )

    assert evidence["sources"]

    for source in evidence["sources"]:
        assert source["provider"] == "musicbrainz"