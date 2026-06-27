from __future__ import annotations

from app.cli.review_queue import ReviewQueueCLI


class FakeQueueService:
    def __init__(self, items):
        self._items = items

    def pending(self):
        return self._items


class FakeDecisionService:
    def __init__(self):
        self.approved = []
        self.rejected = []

    def approve(self, item):
        self.approved.append(item)

    def reject(self, item):
        self.rejected.append(item)


class FakeInput:
    def __init__(self, choices):
        self.choices = list(choices)

    def __call__(self, _prompt):
        return self.choices.pop(0)


def test_approve_pending_item():
    item = {
        "artist_name": "Orbital",
        "provider": "Discogs",
        "confidence": 0.88,
        "match_url": "https://discogs.com/artist/example",
    }

    decisions = FakeDecisionService()
    output = []

    cli = ReviewQueueCLI(
        queue_service=FakeQueueService([item]),
        decision_service=decisions,
        input_func=FakeInput(["a"]),
        output_func=output.append,
    )

    result = cli.run()

    assert result == 0
    assert decisions.approved == [item]
    assert decisions.rejected == []
    assert "Approved." in output


def test_reject_pending_item():
    item = {
        "artist_name": "Orbital",
        "provider": "Discogs",
        "confidence": 0.88,
        "match_url": "https://discogs.com/artist/example",
    }

    decisions = FakeDecisionService()
    output = []

    cli = ReviewQueueCLI(
        queue_service=FakeQueueService([item]),
        decision_service=decisions,
        input_func=FakeInput(["r"]),
        output_func=output.append,
    )

    result = cli.run()

    assert result == 0
    assert decisions.approved == []
    assert decisions.rejected == [item]
    assert "Rejected." in output


def test_skip_does_not_call_decision_service():
    item = {
        "artist_name": "Orbital",
        "provider": "Discogs",
        "confidence": 0.88,
        "match_url": "https://discogs.com/artist/example",
    }

    decisions = FakeDecisionService()
    output = []

    cli = ReviewQueueCLI(
        queue_service=FakeQueueService([item]),
        decision_service=decisions,
        input_func=FakeInput(["s"]),
        output_func=output.append,
    )

    result = cli.run()

    assert result == 0
    assert decisions.approved == []
    assert decisions.rejected == []
    assert "Skipped." in output


def test_quit_stops_processing_remaining_items():
    first = {
        "artist_name": "Orbital",
        "provider": "Discogs",
        "confidence": 0.88,
        "match_url": "https://discogs.com/artist/example",
    }
    second = {
        "artist_name": "Underworld",
        "provider": "MusicBrainz",
        "confidence": 0.91,
        "match_url": "https://musicbrainz.org/artist/example",
    }

    decisions = FakeDecisionService()
    output = []

    cli = ReviewQueueCLI(
        queue_service=FakeQueueService([first, second]),
        decision_service=decisions,
        input_func=FakeInput(["q"]),
        output_func=output.append,
    )

    result = cli.run()

    assert result == 0
    assert decisions.approved == []
    assert decisions.rejected == []
    assert "Quitting review queue." in output


def test_invalid_choice_prompts_again():
    item = {
        "artist_name": "Orbital",
        "provider": "Discogs",
        "confidence": 0.88,
        "match_url": "https://discogs.com/artist/example",
    }

    decisions = FakeDecisionService()
    output = []

    cli = ReviewQueueCLI(
        queue_service=FakeQueueService([item]),
        decision_service=decisions,
        input_func=FakeInput(["x", "a"]),
        output_func=output.append,
    )

    result = cli.run()

    assert result == 0
    assert decisions.approved == [item]
    assert "Invalid choice. Use A, R, S, or Q." in output


def test_no_pending_items():
    decisions = FakeDecisionService()
    output = []

    cli = ReviewQueueCLI(
        queue_service=FakeQueueService([]),
        decision_service=decisions,
        input_func=FakeInput([]),
        output_func=output.append,
    )

    result = cli.run()

    assert result == 0
    assert output == ["No pending review items."]