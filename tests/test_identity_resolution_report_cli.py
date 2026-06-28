from app.cli.identity_resolution_report import IdentityResolutionReportCLI


class FakeStatistics:
    def summarize(self, records):
        return {
            "total": 153,
            "resolved": 128,
            "review": 18,
            "unresolved": 7,
            "resolution_rate": 83.7,
            "review_rate": 11.8,
            "unresolved_rate": 4.6,
            "average_confidence": 0.92,
        }


def test_render_report():
    cli = IdentityResolutionReportCLI(
        statistics_service=FakeStatistics()
    )

    report = cli.render([])

    assert "Identity Resolution Report" in report
    assert "Total Records: 153" in report
    assert "Resolved:" in report
    assert "Review:" in report
    assert "Unresolved:" in report
    assert "83.7%" in report
    assert "11.8%" in report
    assert "4.6%" in report
    assert "Average Confidence: 0.92" in report


def test_run_returns_report(capsys):
    cli = IdentityResolutionReportCLI(
        statistics_service=FakeStatistics()
    )

    report = cli.run([])

    captured = capsys.readouterr()

    assert report == captured.out.strip()