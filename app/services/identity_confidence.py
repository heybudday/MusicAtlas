from __future__ import annotations


class IdentityConfidence:
    """
    Computes confidence scores for identity matches.
    """

    DEFAULT_REVIEW_MARGIN = 0.05

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