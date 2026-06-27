from app.services.identity_enrichment import IdentityEnrichmentService


def test_identity_enrichment_stub():
    service = IdentityEnrichmentService()

    artist = object()
    label = object()

    assert service.enrich_artist(artist) is artist
    assert service.enrich_label(label) is label