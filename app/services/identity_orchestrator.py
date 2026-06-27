from __future__ import annotations

from app.identity_providers.factory import create_provider
from app.services.external_identity_service import ExternalIdentityService
from app.services.identity_confidence import IdentityConfidence


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
        confidence_scorer=None,
    ):
        self.session = session
        self.providers = providers or {}
        self.enrichment_repository = enrichment_repository
        self.provider_priority = provider_priority or self.DEFAULT_PROVIDER_PRIORITY
        self.confidence_scorer = confidence_scorer or IdentityConfidence()
        self.external_identity_service = (
            ExternalIdentityService(session) if session is not None else None
        )

    def _get_provider(self, provider):
        return self.providers.get(provider) or create_provider(provider)

    def _get_cached_result(self, provider, entity_type, query):
        if self.enrichment_repository is None:
            return None

        return self.enrichment_repository.get(
            provider,
            entity_type,
            query,
        )

    def _cache_result(self, result):
        if self.enrichment_repository is None:
            return

        if result.get("matched") is False:
            return

        self.enrichment_repository.upsert(result)

    def lookup_artist(self, artist, provider):
        cached = self._get_cached_result(provider, "artist", artist)
        if cached is not None:
            return cached

        result = self._get_provider(provider).lookup_artist(artist)
        self._cache_result(result)
        return result

    def lookup_label(self, label, provider):
        cached = self._get_cached_result(provider, "label", label)
        if cached is not None:
            return cached

        result = self._get_provider(provider).lookup_label(label)
        self._cache_result(result)
        return result

    def lookup_artist_with_fallback(self, artist, providers):
        for provider in providers:
            try:
                result = self.lookup_artist(artist, provider)
            except Exception:
                continue

            if result.get("matched"):
                return result

        return None

    def lookup_label_with_fallback(self, label, providers):
        for provider in providers:
            try:
                result = self.lookup_label(label, provider)
            except Exception:
                continue

            if result.get("matched"):
                return result

        return None

    def _select_best(self, query, results, confidence_threshold):
        return self.confidence_scorer.select_best(
            query,
            results,
            threshold=confidence_threshold,
        )

    def enrich_artist(
        self,
        artist,
        providers,
        confidence_threshold=0.75,
    ):
        results = []

        for provider in providers:
            result = self.lookup_artist(artist, provider)
            results.append(
                {
                    "provider": provider,
                    "result": result,
                }
            )

        return {
            "results": results,
            "best_match": self._select_best(
                artist,
                results,
                confidence_threshold,
            ),
        }

    def enrich_label(
        self,
        label,
        providers,
        confidence_threshold=0.75,
    ):
        results = []

        for provider in providers:
            result = self.lookup_label(label, provider)
            results.append(
                {
                    "provider": provider,
                    "result": result,
                }
            )

        return {
            "results": results,
            "best_match": self._select_best(
                label,
                results,
                confidence_threshold,
            ),
        }

    def enrich_with_priority(self, entity_type, query, providers=None):
        providers = providers or self.provider_priority

        for provider in providers:
            result = (
                self.lookup_artist(query, provider)
                if entity_type == "artist"
                else self.lookup_label(query, provider)
            )

            if result.get("matched"):
                return {
                    "provider": provider,
                    "result": result,
                }

        return None

    def persist_identity(self, source):
        if self.external_identity_service is None:
            return None

        return self.external_identity_service.get_or_create(source)

    def resolve_artist(self, artist_key, artist_name, providers):
        resolved = self.enrich_artist(artist_name, providers)

        best_match = resolved["best_match"]
        if best_match is not None and best_match["result"].get("matched"):
            self.persist_identity(
                {
                    "source_key": artist_key,
                    "entity_type": "artist",
                    **best_match["result"],
                }
            )

        return resolved

    def resolve_label(self, label_key, label_name, providers):
        resolved = self.enrich_label(label_name, providers)

        best_match = resolved["best_match"]
        if best_match is not None and best_match["result"].get("matched"):
            self.persist_identity(
                {
                    "source_key": label_key,
                    "entity_type": "label",
                    **best_match["result"],
                }
            )

        return resolved