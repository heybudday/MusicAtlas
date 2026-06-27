from app.models.identity_review import IdentityReview
from app.repositories.identity_review_repository import (
    IdentityReviewRepository,
)


def test_create_review(db_session):
    repository = IdentityReviewRepository(db_session)

    review = IdentityReview(
        entity_type="artist",
        entity_key="Jeff Mills",
        provider="discogs",
        candidate_external_id="123",
        candidate_name="Jeff Mills",
        confidence=0.75,
        reason="ambiguous",
        status="pending",
    )

    repository.create(review)

    stored = (
        db_session.query(IdentityReview)
        .filter_by(entity_key="Jeff Mills")
        .one()
    )

    assert stored.provider == "discogs"
    assert stored.status == "pending"


def test_pending_returns_only_pending(db_session):
    repository = IdentityReviewRepository(db_session)

    repository.create(
        IdentityReview(
            entity_type="artist",
            entity_key="A",
            provider="discogs",
            candidate_external_id="1",
            candidate_name="A",
            confidence=0.7,
            reason="ambiguous",
            status="pending",
        )
    )

    repository.create(
        IdentityReview(
            entity_type="artist",
            entity_key="B",
            provider="discogs",
            candidate_external_id="2",
            candidate_name="B",
            confidence=0.8,
            reason="ambiguous",
            status="approved",
        )
    )

    pending = repository.pending()

    assert len(pending) == 1
    assert pending[0].entity_key == "A"


def test_approve_review(db_session):
    repository = IdentityReviewRepository(db_session)

    review = IdentityReview(
        entity_type="artist",
        entity_key="Jeff Mills",
        provider="discogs",
        candidate_external_id="123",
        candidate_name="Jeff Mills",
        confidence=0.75,
        reason="ambiguous",
        status="pending",
    )

    repository.create(review)

    repository.approve(review)

    assert review.status == "approved"


def test_reject_review(db_session):
    repository = IdentityReviewRepository(db_session)

    review = IdentityReview(
        entity_type="artist",
        entity_key="Jeff Mills",
        provider="discogs",
        candidate_external_id="123",
        candidate_name="Jeff Mills",
        confidence=0.75,
        reason="ambiguous",
        status="pending",
    )

    repository.create(review)

    repository.reject(review)

    assert review.status == "rejected"