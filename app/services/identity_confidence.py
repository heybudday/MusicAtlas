from __future__ import annotations


class IdentityConfidence:
    """
    Computes confidence scores for identity matches.
    """

    def score(self, query, result):
        if not result.get("matched"):
            return 0.0

        if result.get("name") == query:
            return 1.0

        return 0.5

    def reason(self, query, result):
        if not result.get("matched"):
            return "not_matched"

        if result.get("name") == query:
            return "exact_name_match"

        return "partial_name_match"

    def select_best(
        self,
        query,
        results,
        threshold=0.0,
    ):
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

        best = max(
            scored,
            key=lambda item: item["confidence"],
        )

        if best["confidence"] < threshold:
            return None

        return best