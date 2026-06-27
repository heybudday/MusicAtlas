from __future__ import annotations


class ReviewDecisionService:
    """
    Applies reviewer decisions to identity review items.
    """

    VALID_STATUSES = {
        "pending",
        "approved",
        "rejected",
    }

    def __init__(
        self,
        enrichment_repository=None,
        audit_history=None,
    ):
        self.enrichment_repository = enrichment_repository
        self.audit_history = audit_history

    def approve(self, review_item):
        review_item["status"] = "approved"

        if self.enrichment_repository:
            self.enrichment_repository.persist(review_item)

        if self.audit_history:
            self.audit_history.record(
                review_item,
                action="approved",
            )

        return review_item

    def reject(self, review_item):
        review_item["status"] = "rejected"

        if self.audit_history:
            self.audit_history.record(
                review_item,
                action="rejected",
            )

        return review_item

    def skip(self, review_item):
        review_item["status"] = "pending"
        return review_item

    def process(self, review_item, decision):
        if decision == "approve":
            return self.approve(review_item)

        if decision == "reject":
            return self.reject(review_item)

        if decision == "skip":
            return self.skip(review_item)

        raise ValueError(f"Unknown review decision: {decision}")