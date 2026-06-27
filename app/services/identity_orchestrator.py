from __future__ import annotations

from app.identity_providers.factory import create_provider
from app.services.external_identity_service import ExternalIdentityService
from app.services.identity_confidence import IdentityConfidence


class IdentityOrchestrator:
    """
    Identity resolution orchestrator:
    - multi-provider enrichment
    - deterministic confidence scoring
    - decision + persistence layer
    """

    DEFAULT_PROVIDER_PRIORITY = ["discogs", "musicbrainz"]
    DEFAULT_PERSIST_THRESHOLD = 0.90
    REVIEW_MARGIN_THRESHOLD = 0.05

    def __init__(
        self,
        session=None,
        providers=None,
        enrichment_repository=None,
        provider_priority=None,
        confidence_scorer=None,
        external_identity_service=None,
    ):
        self.session = session
        self.providers = providers or {}
        self.enrichment_repository = enrichment_repository
        self.provider_priority = provider_priority or self.DEFAULT_PROVIDER_PRIORITY

        self.confidence_scorer = confidence_scorer or IdentityConfidence()

        self.external_identity_service = (
            external_identity_service
            or (ExternalIdentityService(session) if session is not None else None)
        )

    # -------------------------
    # Providers
    # -------------------------
    def _get_provider(self, provider: str):
        return self.providers.get(provider) or create_provider(provider)

    def _get_cached_lookup(self, provider: str, entity_type: str, name: str):
        if self.enrichment_repository is None:
            return None

        if hasattr(self.enrichment_repository, "get"):
            cached = self.enrichment_repository.get(provider, entity_type, name)
            if cached is not None:
                return cached

        if hasattr(self.enrichment_repository, "find"):
            cached = self.enrichment_repository.find(entity_type, name, provider)
            if cached is not None:
                return cached

        return None

    def _save_lookup(
        self,
        provider: str,
        entity_type: str,
        name: str,
        result: dict,
    ):
        if self.enrichment_repository is None:
            return

        enrichment = {
            "provider": provider,
            "entity_type": entity_type,
            "query": name,
            "result": result,
        }

        if hasattr(self.enrichment_repository, "save"):
            self.enrichment_repository.save(provider, entity_type, name, result)
            return

        if hasattr(self.enrichment_repository, "upsert"):
            try:
                self.enrichment_repository.upsert(enrichment)
            except TypeError:
                self.enrichment_repository.upsert(
                    provider=provider,
                    entity_type=entity_type,
                    query=name,
                    result=result,
                )
            return

        if hasattr(self.enrichment_repository, "create"):
            self.enrichment_repository.create(
                provider=provider,
                entity_type=entity_type,
                query=name,
                result=result,
            )
            return

        if hasattr(self.enrichment_repository, "saved"):
            self.enrichment_repository.saved = enrichment

    def lookup_artist(self, name: str, provider: str):
        cached = self._get_cached_lookup(provider, "artist", name)
        if cached is not None:
            return dict(cached)

        provider_obj = self._get_provider(provider)
        result = provider_obj.lookup_artist(name)

        if result is None:
            return None

        result = dict(result)
        self._save_lookup(provider, "artist", name, result)

        return result

    def lookup_label(self, name: str, provider: str):
        cached = self._get_cached_lookup(provider, "label", name)
        if cached is not None:
            return dict(cached)

        provider_obj = self._get_provider(provider)
        result = provider_obj.lookup_label(name)

        if result is None:
            return None

        result = dict(result)
        self._save_lookup(provider, "label", name, result)

        return result

    # -------------------------
    # Enrichment
    # -------------------------
    def enrich_artist(self, name: str, providers: list[str]):
        results = []
        for p in providers:
            result = self.lookup_artist(name, p)
            if result:
                results.append({"provider": p, "result": result})
        return results

    def enrich_label(self, name: str, providers: list[str]):
        results = []
        for p in providers:
            result = self.lookup_label(name, p)
            if result:
                results.append({"provider": p, "result": result})
        return results

    # -------------------------
    # Scoring
    # -------------------------
    def _score(self, query: str, result: dict) -> float:
        if not self.confidence_scorer:
            return 0.0

        if hasattr(self.confidence_scorer, "score"):
            try:
                return float(self.confidence_scorer.score(query, result))
            except Exception:
                return 0.0

        return 0.0

    def _select_best(self, query: str, candidates: list[dict]):
        if hasattr(self.confidence_scorer, "select_best"):
            selected = self.confidence_scorer.select_best(query, candidates)

            if selected is not None:
                return selected

        scored = []
        for c in candidates:
            scored.append(
                {
                    "provider": c["provider"],
                    "result": c["result"],
                    "confidence": self._score(query, c["result"]),
                    "reason": None,
                }
            )

        scored.sort(key=lambda x: x["confidence"], reverse=True)

        if not scored:
            return None

        best = scored[0]
        second = scored[1]["confidence"] if len(scored) > 1 else 0.0
        margin = best["confidence"] - second

        best["confidence_margin"] = margin
        best["review_recommended"] = margin < self.REVIEW_MARGIN_THRESHOLD

        return best

    # -------------------------
    # Resolution
    # -------------------------
    def resolve_artist(self, name: str, providers: list[str] | None = None):
        providers = providers or self.provider_priority
        candidates = self.enrich_artist(name, providers)

        best = self._select_best(name, candidates)

        if best is None:
            best = {
                "provider": None,
                "result": {},
                "confidence": 0.0,
                "reason": None,
                "confidence_margin": 0.0,
                "review_recommended": True,
            }

        confidence_margin = best.get("confidence_margin", 0.0)
        review_recommended = best.get(
            "review_recommended",
            confidence_margin < self.REVIEW_MARGIN_THRESHOLD,
        )

        decision = {
            "confidence_margin": confidence_margin,
            "review_recommended": review_recommended,
            "reason": (
                "ambiguous_identity_match"
                if review_recommended
                else "confident_identity_match"
            ),
        }

        if best.get("reason"):
            decision["match_reason"] = best["reason"]

        result = {
            "provider": best["provider"],
            "result": best["result"],
            "confidence": best["confidence"],
            "decision": decision,
        }

        self._maybe_persist(name, best)

        return result

    def resolve_label(self, name: str, providers: list[str] | None = None):
        return self.resolve_artist(name, providers)

    # -------------------------
    # Persistence
    # -------------------------
    def _maybe_persist(self, name: str, bundle: dict):
        svc = self.external_identity_service
        if not svc:
            return

        confidence = bundle.get("confidence", 0.0)
        if confidence < self.DEFAULT_PERSIST_THRESHOLD:
            return

        payload = {
            "entity_type": "artist",
            "entity_key": name,
            "service": bundle.get("provider"),
            "external_id": bundle.get("result", {}).get("external_id", name),
            "external_url": bundle.get("result", {}).get("url"),
            "confidence": confidence,
        }

        if hasattr(svc, "upsert_artist_identity"):
            svc.upsert_artist_identity(name, bundle.get("result", {}))
            return

        if hasattr(svc, "upsert"):
            svc.upsert(**payload)
        else:
            svc.create(**payload)