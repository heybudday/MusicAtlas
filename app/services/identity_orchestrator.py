from __future__ import annotations

from app.identity_providers.factory import create_provider
from app.services.external_identity_service import ExternalIdentityService


class IdentityOrchestrator:
    """
    Coordinates identity lookups across one or more providers.
    """

    DEFAULT_PROVIDER_PRIORITY = ["discogs", "musicbrainz"]

    def __init__(
        self,
        session=None,
        providers=None,
        enrichment_repository=None,
        provider_priority=None,
    ):
        self.session = session
        self.providers = providers or {}
        self.enrichment_repository = enrichment_repository
        self.provider_priority = provider_priority or self.DEFAULT_PROVIDER_PRIORITY
        self.external_identity_service = (
            ExternalIdentityService(session) if session is not None else None
        )

    def _get_provider(self, provider):
        return self.providers.get(provider) or create_provider(provider)

    def _get_cached_result(self, provider, entity_type, query):
        if self.enrichment_repository is None:
            return None

        return self.enrichment_repository.get(provider, entity_type, query)

    def _cache_result(self, result, matched_only=False):
        if self.enrichment_repository is None:
            return

        if matched_only and result.get("matched") is not True:
            return

        self.enrichment_repository.upsert(result)

    def _find_external_identity(self, entity_type, entity_key, provider):
        if self.external_identity_service is None:
            return None

        return self.external_identity_service.find(
            entity_type,
            entity_key,
            provider,
        )

    def _lookup_artist_uncached(self, artist, provider):
        cached = self._get_cached_result(provider, "artist", artist)
        if cached is not None:
            return cached

        provider_instance = self._get_provider(provider)
        return provider_instance.lookup_artist(artist)

    def _lookup_label_uncached(self, label, provider):
        cached = self._get_cached_result(provider, "label", label)
        if cached is not None:
            return cached

        provider_instance = self._get_provider(provider)
        return provider_instance.lookup_label(label)

    def lookup_artist(self, artist, provider):
        cached = self._get_cached_result(provider, "artist", artist)
        if cached is not None:
            return cached

        external_identity = self._find_external_identity(
            "artist",
            artist,
            provider,
        )
        if external_identity is not None:
            return external_identity

        provider_instance = self._get_provider(provider)
        result = provider_instance.lookup_artist(artist)

        self._cache_result(result)

        return result

    def lookup_label(self, label, provider):
        cached = self._get_cached_result(provider, "label", label)
        if cached is not None:
            return cached

        external_identity = self._find_external_identity(
            "label",
            label,
            provider,
        )
        if external_identity is not None:
            return external_identity

        provider_instance = self._get_provider(provider)
        result = provider_instance.lookup_label(label)

        self._cache_result(result)

        return result

    def lookup_artist_with_fallback(self, artist, providers=None):
        return self._lookup_with_fallback(
            entity_type="artist",
            query=artist,
            providers=providers,
        )

    def lookup_label_with_fallback(self, label, providers=None):
        return self._lookup_with_fallback(
            entity_type="label",
            query=label,
            providers=providers,
        )

    def _lookup_with_fallback(self, entity_type, query, providers=None):
        provider_names = providers or self.provider_priority
        last_result = None

        for provider in provider_names:
            try:
                if entity_type == "artist":
                    result = self._lookup_artist_uncached(query, provider)
                elif entity_type == "label":
                    result = self._lookup_label_uncached(query, provider)
                else:
                    raise ValueError(f"Unsupported entity type: {entity_type}")
            except Exception:
                continue

            last_result = result

            if result.get("matched") is True:
                self._cache_result(result, matched_only=True)
                return result

        if last_result is not None:
            return last_result

        return {
            "matched": False,
            "entity_type": entity_type,
            "query": query,
            "reason": "no_provider_match",
        }

    def enrich_artist(self, artist, providers=None):
        provider_names = providers or self.provider_priority

        return [
            {
                "provider": provider,
                "result": self.lookup_artist(artist, provider),
            }
            for provider in provider_names
        ]

    def enrich_label(self, label, providers=None):
        provider_names = providers or self.provider_priority

        return [
            {
                "provider": provider,
                "result": self.lookup_label(label, provider),
            }
            for provider in provider_names
        ]

    def resolve_artist(self, artist_key, artist_name, providers=None):
        provider_names = providers or self.provider_priority
        results = []

        for provider in provider_names:
            result = self._lookup_artist_uncached(artist_name, provider)

            results.append(
                {
                    "provider": provider,
                    "result": result,
                }
            )

            self._persist_external_identity(
                entity_type="artist",
                entity_key=artist_key,
                provider=provider,
                result=result,
            )

        return results

    def resolve_label(self, label_key, label_name, providers=None):
        provider_names = providers or self.provider_priority
        results = []

        for provider in provider_names:
            result = self._lookup_label_uncached(label_name, provider)

            results.append(
                {
                    "provider": provider,
                    "result": result,
                }
            )

            self._persist_external_identity(
                entity_type="label",
                entity_key=label_key,
                provider=provider,
                result=result,
            )

        return results

    def _persist_external_identity(
        self,
        entity_type,
        entity_key,
        provider,
        result,
    ):
        if self.external_identity_service is None:
            return

        if result.get("matched") is not True:
            return

        self.external_identity_service.upsert(
            entity_type=entity_type,
            entity_key=entity_key,
            service=provider,
            external_id=result.get("external_id"),
            external_url=result.get("url"),
            confidence=result.get("confidence"),
            source="identity_orchestrator",
        )