from app.services.batch_auto_review_runner import BatchAutoReviewRunner


class FakeAutomaticIdentityResolution:
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def resolve(self, artist):
        self.calls.append(artist)

        result = self.results.pop(0)

        if isinstance(result, Exception):
            raise result

        return result


class ResultObject:
    def __init__(self, status):
        self.status = status


def test_processes_multiple_artists():
    resolver = FakeAutomaticIdentityResolution(
        [
            {"status": "resolved"},
            {"status": "review_required"},
            {"status": "skipped"},
        ]
    )

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run(["Artist One", "Artist Two", "Artist Three"])

    assert resolver.calls == ["Artist One", "Artist Two", "Artist Three"]
    assert summary["processed"] == 3


def test_counts_successful_resolutions():
    resolver = FakeAutomaticIdentityResolution(
        [
            {"status": "resolved"},
            {"status": "resolved"},
        ]
    )

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run(["Artist One", "Artist Two"])

    assert summary["processed"] == 2
    assert summary["resolved"] == 2
    assert summary["review_required"] == 0
    assert summary["skipped"] == 0
    assert summary["failed"] == 0


def test_counts_review_required_results():
    resolver = FakeAutomaticIdentityResolution(
        [
            {"status": "review_required"},
            {"status": "review_required"},
        ]
    )

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run(["Artist One", "Artist Two"])

    assert summary["processed"] == 2
    assert summary["resolved"] == 0
    assert summary["review_required"] == 2
    assert summary["skipped"] == 0
    assert summary["failed"] == 0


def test_counts_skipped_results():
    resolver = FakeAutomaticIdentityResolution(
        [
            None,
            {"status": "skipped"},
            {"status": "unknown"},
        ]
    )

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run(["Artist One", "Artist Two", "Artist Three"])

    assert summary["processed"] == 3
    assert summary["resolved"] == 0
    assert summary["review_required"] == 0
    assert summary["skipped"] == 3
    assert summary["failed"] == 0


def test_continues_after_exception():
    resolver = FakeAutomaticIdentityResolution(
        [
            {"status": "resolved"},
            RuntimeError("lookup failed"),
            {"status": "review_required"},
        ]
    )

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run(["Artist One", "Artist Two", "Artist Three"])

    assert resolver.calls == ["Artist One", "Artist Two", "Artist Three"]
    assert summary["processed"] == 3
    assert summary["resolved"] == 1
    assert summary["review_required"] == 1
    assert summary["skipped"] == 0
    assert summary["failed"] == 1
    assert summary["failures"] == [
        {
            "artist": "Artist Two",
            "error": "lookup failed",
        }
    ]


def test_empty_artist_list():
    resolver = FakeAutomaticIdentityResolution([])

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run([])

    assert summary == {
        "processed": 0,
        "resolved": 0,
        "review_required": 0,
        "skipped": 0,
        "failed": 0,
        "failures": [],
    }


def test_respects_limit():
    resolver = FakeAutomaticIdentityResolution(
        [
            {"status": "resolved"},
            {"status": "resolved"},
        ]
    )

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run(["Artist One", "Artist Two", "Artist Three"], limit=2)

    assert resolver.calls == ["Artist One", "Artist Two"]
    assert summary["processed"] == 2
    assert summary["resolved"] == 2


def test_accepts_result_object_with_status_attribute():
    resolver = FakeAutomaticIdentityResolution(
        [
            ResultObject("resolved"),
            ResultObject("review_required"),
        ]
    )

    runner = BatchAutoReviewRunner(automatic_identity_resolution=resolver)

    summary = runner.run(["Artist One", "Artist Two"])

    assert summary["processed"] == 2
    assert summary["resolved"] == 1
    assert summary["review_required"] == 1