from __future__ import annotations


class IdentityResolutionStatistics:
    def __init__(self, repository=None):
        self.repository = repository

    def summarize(self, records=None):
        records = records or []

        total = len(records)
        resolved = self._count_status(records, "resolved")
        review = self._count_status(records, "review")
        unresolved = self._count_status(records, "unresolved")

        pending_review = self._count_status(records, "pending_review")
        auto_resolved = self._count_status(records, "auto_resolved")
        manual_review = self._count_status(records, "manual_review")
        failed = self._count_status(records, "failed")

        confidences = [
            record.get("confidence")
            for record in records
            if record.get("confidence") is not None
        ]

        return {
            "total": total,
            "resolved": resolved,
            "review": review,
            "unresolved": unresolved,
            "pending_review": pending_review,
            "auto_resolved": auto_resolved,
            "manual_review": manual_review,
            "failed": failed,
            "resolution_rate": resolved / total if total else 0.0,
            "review_rate": review / total if total else 0.0,
            "unresolved_rate": unresolved / total if total else 0.0,
            "average_confidence": (
                sum(confidences) / len(confidences) if confidences else 0.0
            ),
            "highest_confidence": max(confidences) if confidences else 0.0,
            "lowest_confidence": min(confidences) if confidences else 0.0,
        }

    def summary(self, records=None):
        if self.repository is not None and records is None:
            total = self.repository.total_artists()
            resolved = self.repository.resolved()

            return {
                "total": total,
                "resolved": resolved,
                "pending_review": self.repository.pending_review(),
                "auto_resolved": self.repository.auto_resolved(),
                "manual_review": self.repository.manual_review(),
                "failed": self.repository.failed(),
                "resolution_rate": resolved / total if total else 0.0,
            }

        return self.summarize(records)

    def _count_status(self, records, status):
        return sum(1 for record in records if record.get("status") == status)