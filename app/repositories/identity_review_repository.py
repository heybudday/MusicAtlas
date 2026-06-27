from __future__ import annotations

from datetime import UTC, datetime

from app.models.identity_review import IdentityReview


class IdentityReviewRepository:
    """
    Repository for identity review queue records.
    """

    def __init__(self, session):
        self.session = session

    def create(self, review):
        self.session.add(review)
        self.session.commit()
        return review

    def get(self, review_id):
        return (
            self.session.query(IdentityReview)
            .filter_by(id=review_id)
            .first()
        )

    def pending(self):
        return (
            self.session.query(IdentityReview)
            .filter_by(status="pending")
            .all()
        )

    def approve(self, review):
        review.status = "approved"
        review.reviewed_at = datetime.now(UTC)
        self.session.commit()
        return review

    def reject(self, review):
        review.status = "rejected"
        review.reviewed_at = datetime.now(UTC)
        self.session.commit()
        return review