from __future__ import annotations

from datetime import datetime

from app.services.identity_audit_dashboard import IdentityAuditDashboard


def test_dashboard_counts_totals_passed_review_and_failed():
    report = [
        {
            "query": "Artist One",
            "matched": True,
            "review_recommended": False,
            "confidence": 0.95,
        },
        {
            "query": "Artist Two",
            "matched": True,
            "review_recommended": True,
            "confidence": 0.82,
        },
        {
            "query": "Artist Three",
            "matched": False,
            "review_recommended": False,
            "confidence": 0.0,
        },
    ]

    summary = IdentityAuditDashboard().summary(report)

    assert summary["total"] == 3
    assert summary["passed"] == 1
    assert summary["review"] == 1
    assert summary["failed"] == 1


def test_dashboard_groups_confidence_buckets():
    report = [
        {"confidence": 0.95},
        {"confidence": 0.90},
        {"confidence": 0.89},
        {"confidence": 0.70},
        {"confidence": 0.69},
        {"confidence": None},
    ]

    summary = IdentityAuditDashboard().summary(report)

    assert summary["confidence"] == {
        "high": 2,
        "medium": 2,
        "low": 2,
    }


def test_dashboard_counts_providers():
    report = [
        {"provider": "discogs"},
        {"provider": "discogs"},
        {"provider": "musicbrainz"},
        {"provider": None},
        {},
    ]

    summary = IdentityAuditDashboard().summary(report)

    assert summary["providers"] == {
        "discogs": 2,
        "musicbrainz": 1,
    }


def test_dashboard_aggregates_issues():
    report = [
        {"issues": ["missing_spotify", "ambiguous_identity"]},
        {"issues": ["missing_spotify"]},
        {"issues": ["missing_bandcamp"]},
        {"issues": []},
        {},
    ]

    summary = IdentityAuditDashboard().summary(report)

    assert summary["issues"] == {
        "ambiguous_identity": 1,
        "missing_bandcamp": 1,
        "missing_spotify": 2,
    }


def test_dashboard_finds_last_audit_timestamp():
    older = datetime(2026, 6, 26, 12, 0, 0)
    newer = datetime(2026, 6, 27, 15, 30, 0)

    report = [
        {"audited_at": older},
        {"audited_at": newer},
        {"audited_at": None},
        {},
    ]

    summary = IdentityAuditDashboard().summary(report)

    assert summary["last_audit"] == newer


def test_dashboard_handles_empty_report():
    summary = IdentityAuditDashboard().summary([])

    assert summary == {
        "total": 0,
        "passed": 0,
        "review": 0,
        "failed": 0,
        "confidence": {
            "high": 0,
            "medium": 0,
            "low": 0,
        },
        "providers": {},
        "issues": {},
        "last_audit": None,
    }


def test_dashboard_handles_none_report():
    summary = IdentityAuditDashboard().summary(None)

    assert summary["total"] == 0
    assert summary["passed"] == 0
    assert summary["review"] == 0
    assert summary["failed"] == 0