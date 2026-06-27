from app.services.identity_confidence import IdentityConfidence


def test_exact_name_match_scores_highest():
    scorer = IdentityConfidence()

    result = {
        "matched": True,
        "name": "Jeff Mills",
    }

    assert scorer.score("Jeff Mills", result) == 1.0
    assert scorer.reason("Jeff Mills", result) == "exact_name_match"


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
        "confidence_margin": 0.5,
        "review_recommended": False,
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
        threshold=0.90,
    )

    assert winner is None


def test_review_recommended_when_margin_is_small():
    scorer = IdentityConfidence()

    results = [
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "name": "Jeff Mills",
            },
        },
        {
            "provider": "discogs",
            "result": {
                "matched": True,
                "name": "Jeff Mills",
            },
        },
    ]

    winner = scorer.select_best(
        "Jeff Mills",
        results,
        review_margin=0.05,
    )

    assert winner["confidence_margin"] == 0.0
    assert winner["review_recommended"] is True


def test_single_provider_does_not_recommend_review():
    scorer = IdentityConfidence()

    results = [
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "name": "Jeff Mills",
            },
        },
    ]

    winner = scorer.select_best("Jeff Mills", results)

    assert winner["confidence_margin"] == 1.0
    assert winner["review_recommended"] is False


def test_large_margin_does_not_recommend_review():
    scorer = IdentityConfidence()

    results = [
        {
            "provider": "musicbrainz",
            "result": {
                "matched": True,
                "name": "Jeff Mills",
            },
        },
        {
            "provider": "discogs",
            "result": {
                "matched": True,
                "name": "Jeff",
            },
        },
    ]

    winner = scorer.select_best("Jeff Mills", results)

    assert winner["confidence_margin"] == 0.5
    assert winner["review_recommended"] is False