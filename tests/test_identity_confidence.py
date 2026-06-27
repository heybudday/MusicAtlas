from app.services.identity_confidence import IdentityConfidence


def test_exact_name_match_scores_highest():
    scorer = IdentityConfidence()

    exact = {
        "matched": True,
        "name": "Jeff Mills",
    }

    partial = {
        "matched": True,
        "name": "Jeff",
    }

    assert scorer.score("Jeff Mills", exact) > scorer.score(
        "Jeff Mills",
        partial,
    )


def test_selects_highest_confidence_result():
    scorer = IdentityConfidence()

    results = [
        {
            "provider": "discogs",
            "result": {
                "matched": True,
                "name": "Jeff",
            },
        },
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "name": "Jeff Mills",
            },
        },
    ]

    winner = scorer.select_best("Jeff Mills", results)

    assert winner == {
        "provider": "musicbrainz",
        "confidence": 1.0,
        "reason": "exact_name_match",
        "result": {
            "matched": True,
            "name": "Jeff Mills",
        },
    }


def test_returns_none_when_best_score_below_threshold():
    scorer = IdentityConfidence()

    results = [
        {
            "provider": "discogs",
            "result": {
                "matched": True,
                "name": "Jeff",
            },
        },
    ]

    winner = scorer.select_best(
        "Jeff Mills",
        results,
        threshold=0.75,
    )

    assert winner is None