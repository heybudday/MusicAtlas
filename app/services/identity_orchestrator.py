from __future__ import annotations

from app.identity_providers.factory import create_provider
from app.services.external_identity_service import ExternalIdentityService
from app.services.identity_confidence import IdentityConfidence


class IdentityOrchestrator:
    """
    Coordinates identity lookups across one or more providers.
    """

    DEFAULT_PROVIDER_PRIORITY = ["discogs", "musicbrainz"]
    DEFAULT_PERSIST_THRESHOLD = 0.90

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
        if self.enrichment_repository is not None:
            self.enrichment_repository.upsert(result)

    def _should_persist_identity(self, best_match):
        if best_match is None:
            return False

        result = best_match.get("result", {})

        return (
            result.get("matched") is True
            and best_match.get("confidence", 0) >= self.DEFAULT_PERSIST_THRESHOLD
        )

    def _summarize_result(self, item):
        result = item.get("result", {})

        return {
            "provider": item.get("provider"),
            "confidence": item.get(
                "confidence",
                result.get("confidence", 0),
            ),
            "reason": item.get(
                "reason",
                result.get("reason"),
            ),
        }

    def _build_decision_summary(self, best_match, results):
        if best_match is None:
            return None

        winner_provider = best_match.get("provider")
        evaluated = [
            self._summarize_result(item)
            for item in results
        ]

        return {
            "provider": winner_provider,
            "confidence": best_match.get("confidence", 0),
            "reason": best_match.get("reason"),
            "evaluated": evaluated,
            "compared_against": [
                item
                for item in evaluated
                if item["provider"] != winner_provider
            ],
        }

    def _build_resolution_result(self, best_match, results):
        if best_match is None:
            return {
                "winner": None,
                "decision": None,
            }

        return {
            **best_match,
            "winner": best_match,
            "decision": self._build_decision_summary(
                best_match,
                results,
            ),
        }

    def lookup_artist(self, artist, provider):
        cached = self._get_cached_result(provider, "artist", artist)
        if cached is not None:
            return cached

        provider_instance = self._get_provider(provider)
        result = provider_instance.lookup_artist(artist)

        self._cache_result(result)

        return result

    def lookup_label(self, label, provider):
        cached = self._get_cached_result(provider, "label", label)
        if cached is not None:
            return cached

        provider_instance = self._get_provider(provider)
        result = provider_instance.lookup_label(label)

        self._cache_result(result)

        return result

    def enrich_artist(self, artist, providers=None):
        providers = providers or self.provider_priority

        return [
            {
                "provider": provider,
                "result": self.lookup_artist(artist, provider),
            }
            for provider in providers
        ]

    def enrich_label(self, label, providers=None):
        providers = providers or self.provider_priority

        return [
            {
                "provider": provider,
                "result": self.lookup_label(label, provider),
            }
            for provider in providers
        ]

    def resolve_artist(self, artist, providers=None):
        results = self.enrich_artist(artist, providers)
        best_match = self.confidence_scorer.select_best(artist, results)

        if (
            self.external_identity_service is not None
            and self._should_persist_identity(best_match)
        ):
            self.external_identity_service.upsert_artist_identity(
                artist,
                best_match,
            )

        return self._build_resolution_result(best_match, results)

    def resolve_label(self, label, providers=None):
        results = self.enrich_label(label, providers)
        best_match = self.confidence_scorer.select_best(label, results)

        if (
            self.external_identity_service is not None
            and self._should_persist_identity(best_match)
        ):
            self.external_identity_service.upsert_label_identity(
                label,
                best_match,
            )

        return self._build_resolution_result(best_match, results)