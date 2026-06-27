from __future__ import annotations


class ReviewMetrics:
    def __init__(self, repository):
        self.repository = repository

    def summary(self):
        pending = self.repository.count_pending()
        approved = self.repository.count_approved()
        rejected = self.repository.count_rejected()
        auto_resolved = self.repository.count_auto_resolved()

        total_reviewed = approved + rejected + auto_resolved
        total = pending + total_reviewed

        review_rate = total_reviewed / total if total else 0

        return {
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "auto_resolved": auto_resolved,
            "total_reviewed": total_reviewed,
            "review_rate": review_rate,
        }