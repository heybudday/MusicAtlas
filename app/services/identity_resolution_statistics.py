from __future__ import annotations


class IdentityResolutionStatistics:
    """
    Computes summary statistics for identity resolution results.
    """

    def summarize(self, records):
        records = records or []

        total = len(records)

        resolved = sum(
            1 for r in records if r.get("status") == "resolved"
        )

        review = sum(
            1 for r in records if r.get("status") == "review"
        )

        unresolved = sum(
            1 for r in records if r.get("status") == "unresolved"
        )

        confidences = [
            r["confidence"]
            for r in records
            if r.get("confidence") is not None
        ]

        if confidences:
            average_confidence = round(
                sum(confidences) / len(confidences),
                3,
            )
            highest_confidence = max(confidences)
            lowest_confidence = min(confidences)
        else:
            average_confidence = 0.0
            highest_confidence = 0.0
            lowest_confidence = 0.0

        if total:
            resolution_rate = resolved / total
            review_rate = review / total
            unresolved_rate = unresolved / total
        else:
            resolution_rate = 0.0
            review_rate = 0.0
            unresolved_rate = 0.0

        return {
            "total": total,
            "resolved": resolved,
            "review": review,
            "unresolved": unresolved,
            "resolution_rate": resolution_rate,
            "review_rate": review_rate,
            "unresolved_rate": unresolved_rate,
            "average_confidence": average_confidence,
            "highest_confidence": highest_confidence,
            "lowest_confidence": lowest_confidence,
        }