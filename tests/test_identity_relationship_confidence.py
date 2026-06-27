from app.services.identity_confidence import IdentityConfidence


def test_exact_alias_match_scores_high():
    scorer = IdentityConfidence()

    result = {
        "matched": True,
        "name": "Richard D. James",
        "related_names": [
            "Aphex Twin",
            "AFX",
            "Polygon Window",
        ],
    }

    assert scorer.score("Aphex Twin", result) == 0.95
    assert scorer.reason("Aphex Twin", result) == "exact_related_name_match"


def test_normalized_alias_match_scores_high():
    scorer = IdentityConfidence()

    result = {
        "matched": True,
        "name": "Richard D. James",
        "related_names": [
            "Aphex Twin",
        ],
    }

    assert scorer.score("  aphex twin  ", result) == 0.92
    assert (
        scorer.reason("  aphex twin  ", result)
        == "normalized_related_name_match"
    )


def test_member_match_scores_high():
    scorer = IdentityConfidence()

    result = {
        "matched": True,
        "name": "Model 500",
        "related_names": [
            "Juan Atkins",
        ],
    }

    assert scorer.score("Juan Atkins", result) == 0.95


def test_group_match_scores_high():
    scorer = IdentityConfidence()

    result = {
        "matched": True,
        "name": "Juan Atkins",
        "related_names": [
            "Model 500",
        ],
    }

    assert scorer.score("Model 500", result) == 0.95


def test_no_relationship_match_falls_back_to_partial():
    scorer = IdentityConfidence()

    result = {
        "matched": True,
        "name": "Richard D. James",
        "related_names": [
            "AFX",
            "Polygon Window",
        ],
    }

    assert scorer.score("Jeff Mills", result) == 0.5
    assert scorer.reason("Jeff Mills", result) == "partial_name_match"


def test_primary_name_beats_alias():
    scorer = IdentityConfidence()

    result = {
        "matched": True,
        "name": "Aphex Twin",
        "related_names": [
            "Richard D. James",
        ],
    }

    assert scorer.score("Aphex Twin", result) > scorer.score(
        "Richard D. James",
        result,
    )


def test_relationship_match_beats_partial_match():
    scorer = IdentityConfidence()

    related_result = {
        "matched": True,
        "name": "Richard D. James",
        "related_names": [
            "Aphex Twin",
        ],
    }

    partial_result = {
        "matched": True,
        "name": "Aphex",
    }

    assert scorer.score(
        "Aphex Twin",
        related_result,
    ) > scorer.score(
        "Aphex Twin",
        partial_result,
    )