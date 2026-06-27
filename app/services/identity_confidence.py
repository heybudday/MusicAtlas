from __future__ import annotations


class IdentityConfidence:
    """
    Computes confidence scores for identity matches.
    """

    DEFAULT_REVIEW_MARGIN = 0.05

    def score(self, query, result):
        if not result.get("matched"):
            return 0.0

        name = result.get("name")

        if name == query:
            return 1.0

        if self._normalize(name) == self._normalize(query):
            return 0.98

        relationship_match = self._related_name_match(query, result)

        if relationship_match == "exact":
            return 0.95

        if relationship_match == "normalized":
            return 0.92

        return 0.5

    def reason(self, query, result):
        if not result.get("matched"):
            return "not_matched"

        name = result.get("name")

        if name == query:
            return "exact_name_match"

        if self._normalize(name) == self._normalize(query):
            return "normalized_name_match"

        relationship_match = self._related_name_match(query, result)

        if relationship_match == "exact":
            return "exact_related_name_match"

        if relationship_match == "normalized":
            return "normalized_related_name_match"

        return "partial_name_match"

    def select_best(
        self,
        query,
        results,
        threshold=0.0,
        review_margin=None,
    ):
        if review_margin is None:
            review_margin = self.DEFAULT_REVIEW_MARGIN

        scored = []

        for item in results:
            result = item["result"]
            confidence = self.score(query, result)

            scored.append(
                {
                    "provider": item["provider"],
                    "confidence": confidence,
                    "reason": self.reason(query, result),
                    "result": result,
                }
            )

        if not scored:
            return None

        ranked = sorted(
            scored,
            key=lambda item: item["confidence"],
            reverse=True,
        )

        best = ranked[0]

        if best["confidence"] < threshold:
            return None

        if len(ranked) > 1:
            confidence_margin = round(
                best["confidence"] - ranked[1]["confidence"],
                2,
            )
        else:
            confidence_margin = 1.0

        best["confidence_margin"] = confidence_margin
        best["review_recommended"] = (
            len(ranked) > 1
            and confidence_margin < review_margin
        )

        return best

    def _related_name_match(self, query, result):
        related_names = result.get("related_names") or []
        query_normalized = self._normalize(query)

        for name in related_names:
            if name == query:
                return "exact"

            if self._normalize(name) == query_normalized:
                return "normalized"

        return None

    def _normalize(self, value):
        return str(value or "").strip().lower()