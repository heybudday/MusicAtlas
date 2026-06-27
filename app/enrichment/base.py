from abc import ABC, abstractmethod

from app.models.enrichment_result import EnrichmentResult


class EnrichmentProvider(ABC):

    @abstractmethod
    def enrich_artist(self, external_id: str) -> EnrichmentResult:
        pass

    @abstractmethod
    def enrich_label(self, external_id: str) -> EnrichmentResult:
        pass