from app.enrichment.base import EnrichmentProvider
from app.clients.musicbrainz import MusicBrainzClient
from app.models.enrichment_result import EnrichmentResult


class MusicBrainzEnrichmentProvider(EnrichmentProvider):

    def __init__(self, client: MusicBrainzClient | None = None):
        self.client = client or MusicBrainzClient()

    def enrich_artist(self, external_id: str) -> EnrichmentResult:
        try:
            artist = self.client.get_artist(external_id)

            return EnrichmentResult(
                provider="musicbrainz",
                success=True,
                data=artist,
                errors=[],
            )

        except Exception as exc:
            return EnrichmentResult(
                provider="musicbrainz",
                success=False,
                data={},
                errors=[str(exc)],
            )

    def enrich_label(self, external_id: str) -> EnrichmentResult:
        return EnrichmentResult(
            provider="musicbrainz",
            success=True,
            data={},
            errors=[],
        )