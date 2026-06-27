from app.models.identity_review import IdentityReview
from app.repositories.identity_review_repository import (
    IdentityReviewRepository,
)


class IdentityReviewService:
    def __init__(self, session):
        self.repository = IdentityReviewRepository(session)

    def create(
        self,
        entity_type: str,
        entity_key: str,
        provider: str,
        candidate_external_id: str | None = None,
        candidate_name: str | None = None,
        confidence: float | None = None,
        reason: str | None = None,
        status: str = "pending",
        review_notes: str | None = None,
    ):
        review = IdentityReview(
            entity_type=entity_type,
            entity_key=entity_key,
            provider=provider,
            candidate_external_id=candidate_external_id,
            candidate_name=candidate_name,
            confidence=confidence,
            reason=reason,
            status=status,
            review_notes=review_notes,
        )

        return self.repository.create(review)

    def pending(self):
        return self.repository.pending()

    def approve(self, review):
        return self.repository.approve(review)

    def reject(self, review):
        return self.repository.reject(review)