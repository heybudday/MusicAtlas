from __future__ import annotations

from app.models.identity_review import IdentityReview
from app.repositories.identity_review_repository import (
    IdentityReviewRepository,
)


class IdentityReviewService:
    """
    Business logic for the human review queue.
    """

    def __init__(self, session):
        self.repository = IdentityReviewRepository(session)

    def enqueue(
        self,
        entity_type,
        entity_key,
        provider,
        candidate_external_id,
        candidate_name,
        confidence,
        reason,
    ):
        review = IdentityReview(
            entity_type=entity_type,
            entity_key=entity_key,
            provider=provider,
            candidate_external_id=candidate_external_id,
            candidate_name=candidate_name,
            confidence=confidence,
            reason=reason,
            status="pending",
        )

        return self.repository.create(review)

    def pending(self):
        return self.repository.pending()

    def approve(self, review):
        return self.repository.approve(review)

    def reject(self, review):
        return self.repository.reject(review)