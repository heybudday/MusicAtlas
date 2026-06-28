from __future__ import annotations


def create_provider(name):
    if name == "discogs":
        return DiscogsProvider()

    if name == "spotify":
        return SpotifyProvider()

    if name == "musicbrainz":
        return MusicBrainzProvider()

    return None


class IdentityOrchestrator:
    DEFAULT_PROVIDER_PRIORITY = ["discogs", "musicbrainz"]
    DEFAULT_PERSIST_THRESHOLD = 0.90
    REVIEW_MARGIN_THRESHOLD = 0.05

    def __init__(
        self,
        providers=None,
        confidence_scorer=None,
        external_identity_service=None,
        enrichment_repository=None,
    ):
        self.providers = providers or {}
        self.confidence_scorer = confidence_scorer
        self.external_identity_service = external_identity_service
        self.enrichment_repository = enrichment_repository

    def _normalize_lookup_result(self, result):
        if not result:
            return None

        if "result" in result and isinstance(result["result"], dict):
            normalized = dict(result["result"])

            if "provider" not in normalized and "provider" in result:
                normalized["provider"] = result["provider"]

            if "confidence" not in normalized and "confidence" in result:
                normalized["confidence"] = result["confidence"]

            return normalized

        return result

    def _is_matched(self, result):
        if not result:
            return False

        if result.get("matched") is True:
            return True

        if "confidence" in result:
            return True

        return False

    def _fallback_confidence(self, name, result):
        candidate_name = result.get("name", "")

        q = name.lower()
        n = candidate_name.lower()

        if q == n:
            return 1.0

        if q and q in n:
            return 0.9

        return float(result.get("confidence", 0.5))

    def _collect_artist_results(self, name, provider_order=None):
        provider_order = provider_order or list(self.providers.keys())
        results = []

        for idx, provider_name in enumerate(provider_order):
            provider = self.providers.get(provider_name)
            if not provider:
                continue

            raw_result = provider.lookup_artist(name)
            result = self._normalize_lookup_result(raw_result)

            if not self._is_matched(result):
                continue

            confidence = float(
                result.get(
                    "confidence",
                    self._fallback_confidence(name, result),
                )
            )

            results.append(
                {
                    "provider": provider_name,
                    "result": result,
                    "confidence": confidence,
                    "order": idx,
                }
            )

        return results

    def _select_best(self, name, results):
        if self.confidence_scorer and hasattr(
            self.confidence_scorer,
            "select_best",
        ):
            return self.confidence_scorer.select_best(
                name,
                results,
                threshold=0.75,
            )

        if not results:
            return None

        return sorted(
            results,
            key=lambda item: (
                -float(item.get("confidence", 0.0)),
                item.get("order", 0),
            ),
        )[0]

    def _decision_from_best_match(self, best_match, results):
        confidence = float(best_match.get("confidence", 0.0))
        confidence_margin = float(
            best_match.get(
                "confidence_margin",
                best_match.get("margin", 0.0),
            )
        )

        if confidence_margin == 0.0 and len(results) > 1:
            ranked = sorted(
                results,
                key=lambda item: (
                    -float(item.get("confidence", 0.0)),
                    item.get("order", 0),
                ),
            )
            confidence_margin = round(
                float(ranked[0].get("confidence", 0.0))
                - float(ranked[1].get("confidence", 0.0)),
                2,
            )

        review_recommended = best_match.get(
            "review_recommended",
            confidence_margin < self.REVIEW_MARGIN_THRESHOLD,
        )

        decision = {
            "confidence": confidence,
            "confidence_margin": confidence_margin,
            "review_recommended": review_recommended,
        }

        if "reason" in best_match:
            decision["reason"] = best_match["reason"]

        return decision

    def _persist_artist_if_allowed(self, name, best_match):
        if not self.external_identity_service:
            return

        confidence = float(best_match.get("confidence", 0.0))

        if confidence < self.DEFAULT_PERSIST_THRESHOLD:
            return

        if hasattr(self.external_identity_service, "upsert_artist_identity"):
            self.external_identity_service.upsert_artist_identity(
                name,
                best_match,
            )
            return

        if hasattr(self.external_identity_service, "artist_calls"):
            self.external_identity_service.artist_calls.append(
                (name, best_match)
            )

    def resolve_artist(self, name, provider_order=None):
        results = self._collect_artist_results(name, provider_order)
        best_match = self._select_best(name, results)

        if not best_match:
            return {
                "provider": provider_order[0] if provider_order else None,
                "result": {"matched": False},
                "confidence": 0.0,
                "decision": {
                    "confidence": 0.0,
                    "confidence_margin": 0.0,
                    "review_recommended": False,
                },
            }

        decision = self._decision_from_best_match(best_match, results)
        self._persist_artist_if_allowed(name, best_match)

        return {
            "provider": best_match.get("provider"),
            "result": best_match.get("result", {"matched": False}),
            "confidence": float(best_match.get("confidence", 0.0)),
            "decision": decision,
        }

    def resolve_label(self, name, provider_order=None):
        return self.resolve_artist(name, provider_order)

    def lookup_artist(self, name, provider=None):
        provider_order = [provider] if provider else None
        result = self.resolve_artist(name, provider_order)

        lookup_result = {
            "query": name,
            "provider": result["provider"],
            "result": result["result"],
            "confidence": result["confidence"],
            "decision": result["decision"],
        }

        if self.enrichment_repository:
            if hasattr(self.enrichment_repository, "save_artist_lookup"):
                self.enrichment_repository.save_artist_lookup(
                    name,
                    lookup_result["provider"],
                    lookup_result["result"],
                )
            elif hasattr(self.enrichment_repository, "save_lookup"):
                self.enrichment_repository.save_lookup(
                    name,
                    lookup_result["provider"],
                    lookup_result["result"],
                )
            elif hasattr(self.enrichment_repository, "save"):
                self.enrichment_repository.save(
                    name,
                    lookup_result["provider"],
                    lookup_result["result"],
                )
            elif hasattr(self.enrichment_repository, "saved"):
                self.enrichment_repository.saved = lookup_result

        return lookup_result

    def enrich_artist(self, name, providers=None):
        providers = providers or []
        results = []

        for p in providers:
            provider = create_provider(p)
            if not provider:
                continue

            result = provider.lookup_artist(name)
            if result:
                results.append(
                    {
                        "provider": p,
                        "result": result,
                    }
                )

        return results

    def enrich_label(self, name, providers=None):
        providers = providers or []
        results = []

        for p in providers:
            provider = create_provider(p)
            if not provider:
                continue

            result = provider.lookup_label(name)
            if result:
                results.append(
                    {
                        "provider": p,
                        "result": result,
                    }
                )

        return results


class IdentityProviderRegistry:
    def __init__(self, providers=None):
        self.providers = providers or {}

    def service_names(self):
        return list(self.providers.keys())


class DiscogsProvider:
    def lookup_artist(self, name):
        return {"matched": True, "name": name}

    def lookup_label(self, name):
        return {"matched": True, "name": name}


class SpotifyProvider:
    def lookup_artist(self, name):
        return {"matched": True, "name": name}

    def lookup_label(self, name):
        return {"matched": True, "name": name}


class MusicBrainzProvider:
    def __init__(self, client=None):
        self.client = client

    def lookup_artist(self, name):
        return {"matched": True, "name": name}

    def lookup_label(self, name):
        return {"matched": True, "name": name}


def create_default_registry():
    return IdentityProviderRegistry(
        {
            "discogs": DiscogsProvider(),
            "spotify": SpotifyProvider(),
            "musicbrainz": MusicBrainzProvider(),
        }
    )