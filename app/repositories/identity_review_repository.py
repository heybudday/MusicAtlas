from app.models.identity_review import IdentityReview


class IdentityReviewRepository:
    def __init__(self, session):
        self.session = session

    def create(self, review):
        self.session.add(review)
        self.session.commit()
        return review

    def pending(self):
        return (
            self.session.query(IdentityReview)
            .filter_by(status="pending")
            .all()
        )

    def approve(self, review):
        review.status = "approved"
        self.session.commit()
        return review

    def reject(self, review):
        review.status = "rejected"
        self.session.commit()
        return review