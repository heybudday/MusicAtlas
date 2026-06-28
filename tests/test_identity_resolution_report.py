from app.services.identity_resolution_report import IdentityResolutionReport


def sample_statistics():
    return {
        "total": 100,
        "resolved": 82,
        "review": 12,
        "unresolved": 6,
        "resolution_rate": 82.0,
        "review_rate": 12.0,
        "unresolved_rate": 6.0,
        "average_confidence": 0.91,
    }


def test_generate_returns_string():
    report = IdentityResolutionReport()

    result = report.generate(sample_statistics())

    assert isinstance(result, str)


def test_report_contains_title():
    report = IdentityResolutionReport()

    result = report.generate(sample_statistics())

    assert "Identity Resolution Report" in result


def test_report_contains_total_records():
    report = IdentityResolutionReport()

    result = report.generate(sample_statistics())

    assert "Total Records: 100" in result


def test_report_contains_status_counts():
    report = IdentityResolutionReport()

    result = report.generate(sample_statistics())

    assert "Resolved:" in result
    assert "Review:" in result
    assert "Unresolved:" in result


def test_report_contains_percentages():
    report = IdentityResolutionReport()

    result = report.generate(sample_statistics())

    assert "82.0%" in result
    assert "12.0%" in result
    assert "6.0%" in result


def test_report_contains_average_confidence():
    report = IdentityResolutionReport()

    result = report.generate(sample_statistics())

    assert "Average Confidence: 0.91" in result


def test_empty_statistics():
    report = IdentityResolutionReport()

    result = report.generate(
        {
            "total": 0,
            "resolved": 0,
            "review": 0,
            "unresolved": 0,
            "resolution_rate": 0.0,
            "review_rate": 0.0,
            "unresolved_rate": 0.0,
            "average_confidence": 0.0,
        }
    )

    assert "Total Records: 0" in result
    assert "0.0%" in result
    assert "Average Confidence: 0.00" in result


def test_report_is_deterministic():
    report = IdentityResolutionReport()

    first = report.generate(sample_statistics())
    second = report.generate(sample_statistics())

    assert first == second