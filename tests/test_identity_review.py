from app.services.identity_review import IdentityReviewService


def test_enqueue_review(db_session):
    service = IdentityReviewService(db_session)

    review = service.enqueue(
        entity_type="artist",
        entity_key="Jeff Mills",
        provider="discogs",
        candidate_external_id="123",
        candidate_name="Jeff Mills",
        confidence=0.75,
        reason="ambiguous",
    )

    assert review.status == "pending"
    assert review.entity_key == "Jeff Mills"


def test_pending_reviews(db_session):
    service = IdentityReviewService(db_session)

    service.enqueue(
        entity_type="artist",
        entity_key="Jeff Mills",
        provider="discogs",
        candidate_external_id="123",
        candidate_name="Jeff Mills",
        confidence=0.75,
        reason="ambiguous",
    )

    pending = service.pending()

    assert len(pending) == 1
    assert pending[0].status == "pending"


def test_approve_review(db_session):
    service = IdentityReviewService(db_session)

    review = service.enqueue(
        entity_type="artist",
        entity_key="Jeff Mills",
        provider="discogs",
        candidate_external_id="123",
        candidate_name="Jeff Mills",
        confidence=0.75,
        reason="ambiguous",
    )

    service.approve(review)

    assert review.status == "approved"
    assert review.reviewed_at is not None


def test_reject_review(db_session):
    service = IdentityReviewService(db_session)

    review = service.enqueue(
        entity_type="artist",
        entity_key="Jeff Mills",
        provider="discogs",
        candidate_external_id="123",
        candidate_name="Jeff Mills",
        confidence=0.75,
        reason="ambiguous",
    )

    service.reject(review)

    assert review.status == "rejected"
    assert review.reviewed_at is not None