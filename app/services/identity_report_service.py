from __future__ import annotations

from app.services.identity_resolution_statistics import (
    IdentityResolutionStatistics,
)


class IdentityReportService:
    """
    Builds an identity resolution report from repository data.
    """

    def __init__(self, repository=None, statistics=None):
        self.repository = repository
        self.statistics = (
            statistics
            if statistics is not None
            else IdentityResolutionStatistics()
        )

    def generate_report(self):
        """
        Generate an identity resolution report.

        Returns the statistics summary for all identity resolution records.
        """
        records = []

        if self.repository is not None:
            records = self.repository.all()

        return self.statistics.summarize(records)