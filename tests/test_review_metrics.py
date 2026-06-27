from app.services.review_metrics import ReviewMetrics


class FakeReviewRepository:
    def __init__(
        self,
        pending=0,
        approved=0,
        rejected=0,
        auto_resolved=0,
    ):
        self.pending = pending
        self.approved = approved
        self.rejected = rejected
        self.auto_resolved = auto_resolved

    def count_pending(self):
        return self.pending

    def count_approved(self):
        return self.approved

    def count_rejected(self):
        return self.rejected

    def count_auto_resolved(self):
        return self.auto_resolved


def test_review_metrics_empty_queue():
    repository = FakeReviewRepository()

    metrics = ReviewMetrics(repository).summary()

    assert metrics["pending"] == 0
    assert metrics["approved"] == 0
    assert metrics["rejected"] == 0
    assert metrics["auto_resolved"] == 0
    assert metrics["total_reviewed"] == 0
    assert metrics["review_rate"] == 0


def test_review_metrics_mixed_queue():
    repository = FakeReviewRepository(
        pending=25,
        approved=50,
        rejected=10,
        auto_resolved=15,
    )

    metrics = ReviewMetrics(repository).summary()

    assert metrics["pending"] == 25
    assert metrics["approved"] == 50
    assert metrics["rejected"] == 10
    assert metrics["auto_resolved"] == 15
    assert metrics["total_reviewed"] == 75
    assert metrics["review_rate"] == 0.75


def test_review_metrics_everything_completed():
    repository = FakeReviewRepository(
        pending=0,
        approved=80,
        rejected=10,
        auto_resolved=10,
    )

    metrics = ReviewMetrics(repository).summary()

    assert metrics["pending"] == 0
    assert metrics["approved"] == 80
    assert metrics["rejected"] == 10
    assert metrics["auto_resolved"] == 10
    assert metrics["total_reviewed"] == 100
    assert metrics["review_rate"] == 1.0