from __future__ import annotations

from app.services.identity_resolution_statistics import (
    IdentityResolutionStatistics,
)


class IdentityResolutionReportCLI:
    """
    Command-line report for identity resolution statistics.
    """

    def __init__(self, statistics_service=None):
        self.statistics_service = (
            statistics_service
            or IdentityResolutionStatistics()
        )

    def render(self, records):
        summary = self.statistics_service.summarize(records)

        lines = [
            "Identity Resolution Report",
            "=" * 26,
            "",
            f"Total Records: {summary['total']}",
            "",
            f"Resolved:    {summary['resolved']:>5} ({summary['resolution_rate']:.1f}%)",
            f"Review:      {summary['review']:>5} ({summary['review_rate']:.1f}%)",
            f"Unresolved:  {summary['unresolved']:>5} ({summary['unresolved_rate']:.1f}%)",
            "",
            f"Average Confidence: {summary['average_confidence']:.2f}",
        ]

        return "\n".join(lines)

    def run(self, records):
        report = self.render(records)
        print(report)
        return report