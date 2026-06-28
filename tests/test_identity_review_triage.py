import pytest

from app.services.identity_review_triage import IdentityReviewTriage


def test_auto_resolve_high_confidence():
    triage = IdentityReviewTriage()

    result = triage.triage({
        "confidence": 0.95,
        "provider_scores": {"discogs": 0.9, "musicbrainz": 0.92},
        "evidence": {
            "official_url": True,
            "spotify_match": True,
            "social_links": True
        }
    })

    assert result.decision == "AUTO_RESOLVE"


def test_escalate_low_confidence():
    triage = IdentityReviewTriage()

    result = triage.triage({
        "confidence": 0.50,
        "provider_scores": {"discogs": 0.6, "musicbrainz": 0.4},
        "evidence": {}
    })

    assert result.decision == "ESCALATE"


def test_provider_conflict_triggers_penalty():
    triage = IdentityReviewTriage()

    result = triage.triage({
        "confidence": 0.85,
        "provider_scores": {"discogs": 0.95, "musicbrainz": 0.60},
        "evidence": {
            "official_url": True,
            "spotify_match": False,
            "social_links": False
        }
    })

    assert "provider_conflict" in result.reason_codes