import json

from app.cli.review_queue import format_table, main


class FakeQueue:
    def __init__(self, items):
        self._items = items

    def pending(self):
        return self._items


def test_format_table_empty():
    output = format_table([])

    assert "No artists currently require manual review." in output
    assert "Pending Reviews: 0" in output


def test_format_table_with_items():
    output = format_table(
        [
            {
                "artist_id": 12,
                "artist_name": "Orbital",
                "confidence": 0.88,
                "providers": ["discogs", "musicbrainz"],
            },
            {
                "artist_id": 18,
                "artist_name": "Sasha",
                "confidence": 0.91,
                "providers": ["discogs"],
            },
        ]
    )

    assert "Pending Reviews: 2" in output
    assert "Orbital" in output
    assert "Sasha" in output
    assert "discogs,musicbrainz" in output


def test_cli_json(monkeypatch, capsys):
    from app.cli import review_queue

    monkeypatch.setattr(
        review_queue,
        "HumanReviewQueue",
        lambda: FakeQueue(
            [
                {
                    "artist_id": 1,
                    "artist_name": "Phoenix",
                    "confidence": 0.87,
                    "providers": ["musicbrainz"],
                }
            ]
        ),
    )

    assert main(["--json"]) == 0

    captured = capsys.readouterr()

    data = json.loads(captured.out)

    assert data[0]["artist_name"] == "Phoenix"
    assert data[0]["confidence"] == 0.87