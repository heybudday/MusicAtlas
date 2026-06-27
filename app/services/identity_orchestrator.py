from __future__ import annotations

from app.identity_providers.factory import create_provider
from app.services.external_identity_service import ExternalIdentityService


class IdentityOrchestrator:
    """
    Coordinates identity lookups across one or more providers.
    """

    def __init__(self, session=None):
        self.session = session
        self.external_identity_service = (
            ExternalIdentityService(session) if session is not None else None
        )

    def enrich_artist(self, artist, providers):
        results = []

        for provider_name in providers:
            provider = create_provider(provider_name)
            result = provider.lookup_artist(artist)

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
            provider = create_provider(provider_name)
            result = provider.lookup_label(label)

            results.append(
                {
                    "provider": provider_name,
                    "result": result,
                }
            )

        return results

    def resolve_artist(self, artist_key, artist_name, providers):
        results = self.enrich_artist(artist_name, providers)

        if self.external_identity_service is None:
            return results

        for item in results:
            provider_name = item["provider"]
            result = item["result"]

            if not result.get("matched"):
                continue

            self.external_identity_service.upsert(
                entity_type="artist",
                entity_key=artist_key,
                service=provider_name,
                external_id=result["external_id"],
                external_url=result.get("url"),
                confidence=result.get("confidence", 1.0),
                source="identity_orchestrator",
            )

        return results

    def resolve_label(self, label_key, label_name, providers):
        results = self.enrich_label(label_name, providers)

        if self.external_identity_service is None:
            return results

        for item in results:
            provider_name = item["provider"]
            result = item["result"]

            if not result.get("matched"):
                continue

            self.external_identity_service.upsert(
                entity_type="label",
                entity_key=label_key,
                service=provider_name,
                external_id=result["external_id"],
                external_url=result.get("url"),
                confidence=result.get("confidence", 1.0),
                source="identity_orchestrator",
            )

        return results
