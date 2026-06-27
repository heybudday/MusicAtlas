from app.enrichment.base import EnrichmentProvider
from app.models.enrichment_result import EnrichmentResult


class MusicBrainzEnrichmentProvider(EnrichmentProvider):

    def enrich_artist(self, external_id: str) -> EnrichmentResult:
        return EnrichmentResult(
            provider="musicbrainz",
            success=True,
            data={},
            errors=[],
        )

    def enrich_label(self, external_id: str) -> EnrichmentResult:
        return EnrichmentResult(
            provider="musicbrainz",
            success=True,
            data={},
            errors=[],
        )