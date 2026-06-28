from app.services.identity_resolution_statistics import (
    IdentityResolutionStatistics,
)


def test_empty_dataset():
    stats = IdentityResolutionStatistics()

    result = stats.summarize([])

    assert result["total"] == 0
    assert result["resolved"] == 0
    assert result["review"] == 0
    assert result["unresolved"] == 0

    assert result["resolution_rate"] == 0.0
    assert result["review_rate"] == 0.0
    assert result["unresolved_rate"] == 0.0

    assert result["average_confidence"] == 0.0
    assert result["highest_confidence"] == 0.0
    assert result["lowest_confidence"] == 0.0


def test_all_resolved():
    stats = IdentityResolutionStatistics()

    records = [
        {"status": "resolved", "confidence": 0.95},
        {"status": "resolved", "confidence": 0.90},
    ]

    result = stats.summarize(records)

    assert result["resolved"] == 2
    assert result["review"] == 0
    assert result["unresolved"] == 0
    assert result["resolution_rate"] == 1.0


def test_mixed_status_counts():
    stats = IdentityResolutionStatistics()

    records = [
        {"status": "resolved", "confidence": 0.95},
        {"status": "review", "confidence": 0.72},
        {"status": "review", "confidence": 0.70},
        {"status": "unresolved", "confidence": 0.40},
    ]

    result = stats.summarize(records)

    assert result["total"] == 4
    assert result["resolved"] == 1
    assert result["review"] == 2
    assert result["unresolved"] == 1

    assert result["resolution_rate"] == 0.25
    assert result["review_rate"] == 0.50
    assert result["unresolved_rate"] == 0.25


def test_average_confidence():
    stats = IdentityResolutionStatistics()

    records = [
        {"status": "resolved", "confidence": 0.80},
        {"status": "resolved", "confidence": 0.90},
        {"status": "resolved", "confidence": 1.00},
    ]

    result = stats.summarize(records)

    assert result["average_confidence"] == 0.9


def test_highest_and_lowest_confidence():
    stats = IdentityResolutionStatistics()

    records = [
        {"status": "resolved", "confidence": 0.61},
        {"status": "resolved", "confidence": 0.97},
        {"status": "resolved", "confidence": 0.83},
    ]

    result = stats.summarize(records)

    assert result["highest_confidence"] == 0.97
    assert result["lowest_confidence"] == 0.61


def test_missing_confidence_is_ignored():
    stats = IdentityResolutionStatistics()

    records = [
        {"status": "resolved", "confidence": 1.0},
        {"status": "review"},
        {"status": "resolved", "confidence": 0.8},
        {"status": "unresolved", "confidence": None},
    ]

    result = stats.summarize(records)

    assert result["average_confidence"] == 0.9
    assert result["highest_confidence"] == 1.0
    assert result["lowest_confidence"] == 0.8


def test_none_records_returns_empty_statistics():
    stats = IdentityResolutionStatistics()

    result = stats.summarize(None)

    assert result["total"] == 0
    assert result["resolution_rate"] == 0.0