from __future__ import annotations

from app.identity_providers.factory import create_provider
from app.services.external_identity_service import ExternalIdentityService


class IdentityOrchestrator:
    """
    Coordinates identity lookups across one or more providers.
    """

    def __init__(
        self,
        session=None,
        providers=None,
        enrichment_repository=None,
    ):
        self.session = session
        self.providers = providers or {}
        self.enrichment_repository = enrichment_repository
        self.external_identity_service = (
            ExternalIdentityService(session) if session is not None else None
        )

    def lookup_artist(self, artist, provider):
        if self.enrichment_repository is not None:
            cached = self.enrichment_repository.get(
                provider,
                "artist",
                artist,
            )
            if cached is not None:
                return cached

        provider_instance = (
            self.providers.get(provider)
            or create_provider(provider)
        )

        result = provider_instance.lookup_artist(artist)

        if self.enrichment_repository is not None:
            self.enrichment_repository.upsert(result)

        return result

    def lookup_label(self, label, provider):
        if self.enrichment_repository is not None:
            cached = self.enrichment_repository.get(
                provider,
                "label",
                label,
            )
            if cached is not None:
                return cached

        provider_instance = (
            self.providers.get(provider)
            or create_provider(provider)
        )

        result = provider_instance.lookup_label(label)

        if self.enrichment_repository is not None:
            self.enrichment_repository.upsert(result)

        return result

    def enrich_artist(self, artist, providers):
        results = []

        for provider_name in providers:
            provider = (
                self.providers.get(provider_name)
                or create_provider(provider_name)
            )

            result = provider.lookup_artist(artist)

            if (
                self.enrichment_repository is not None
                and result.get("matched")
            ):
                self.enrichment_repository.upsert(result)

            results.append(
                {
                    "provider": provider_name,
                    "result": result,
                }
            )

        return results

    def enrich_label(self, label, providers):
        results = []

        for provider_name in providers:
            provider = (
                self.providers.get(provider_name)
                or create_provider(provider_name)
            )

            result = provider.lookup_label(label)

            if (
                self.enrichment_repository is not None
                and result.get("matched")
            ):
                self.enrichment_repository.upsert(result)

            results.append(
                {
                    "provider": provider_name,
                    "result": result,
                }
            )

        return results

    def resolve_artist(self, artist_key, artist_name, providers):
        results = self.enrich_artist(artist_name, providers)

        for item in results:
            provider_name = item["provider"]
            result = item["result"]

            if result.get("matched") and self.external_identity_service is not None:
                self.external_identity_service.upsert(
                    entity_type="artist",
                    entity_key=artist_key,
                    service=provider_name,
                    external_id=result.get("external_id"),
                    external_url=result.get("url"),
                    confidence=result.get("confidence"),
                    source="identity_orchestrator",
                )

        return results

    def resolve_label(self, label_key, label_name, providers):
        results = self.enrich_label(label_name, providers)

        for item in results:
            provider_name = item["provider"]
            result = item["result"]

            if result.get("matched") and self.external_identity_service is not None:
                self.external_identity_service.upsert(
                    entity_type="label",
                    entity_key=label_key,
                    service=provider_name,
                    external_id=result.get("external_id"),
                    external_url=result.get("url"),
                    confidence=result.get("confidence"),
                    source="identity_orchestrator",
                )

        return results