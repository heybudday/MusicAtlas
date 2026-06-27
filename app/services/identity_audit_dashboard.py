from __future__ import annotations

from collections import Counter


class IdentityAuditDashboard:
    """
    Summarizes identity audit report rows into dashboard-level metrics.
    """

    HIGH_CONFIDENCE_THRESHOLD = 0.90
    MEDIUM_CONFIDENCE_THRESHOLD = 0.70

    def summary(self, report):
        items = list(report or [])

        return {
            "total": len(items),
            "passed": self._count_passed(items),
            "review": self._count_review(items),
            "failed": self._count_failed(items),
            "confidence": self._confidence_summary(items),
            "providers": self._provider_summary(items),
            "issues": self._issue_summary(items),
            "last_audit": self._last_audit(items),
        }

    def _count_passed(self, items):
        return sum(
            1
            for item in items
            if item.get("matched") and not item.get("review_recommended")
        )

    def _count_review(self, items):
        return sum(1 for item in items if item.get("review_recommended"))

    def _count_failed(self, items):
        return sum(1 for item in items if not item.get("matched"))

    def _confidence_summary(self, items):
        summary = {
            "high": 0,
            "medium": 0,
            "low": 0,
        }

        for item in items:
            confidence = item.get("confidence", 0.0) or 0.0

            if confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
                summary["high"] += 1
            elif confidence >= self.MEDIUM_CONFIDENCE_THRESHOLD:
                summary["medium"] += 1
            else:
                summary["low"] += 1

        return summary

    def _provider_summary(self, items):
        providers = Counter()

        for item in items:
            provider = item.get("provider")

            if provider:
                providers[provider] += 1

        return dict(sorted(providers.items()))

    def _issue_summary(self, items):
        issues = Counter()

        for item in items:
            for issue in item.get("issues", []) or []:
                issues[issue] += 1

        return dict(sorted(issues.items()))

    def _last_audit(self, items):
        timestamps = [
            item.get("audited_at")
            for item in items
            if item.get("audited_at") is not None
        ]

        if not timestamps:
            return None

        return max(timestamps)