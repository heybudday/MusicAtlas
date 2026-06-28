class IdentityResolutionReport:
    """
    Formats identity resolution statistics into a human-readable report.
    """

    def generate(self, statistics):
        return "\n".join(
            [
                "Identity Resolution Report",
                "==========================",
                "",
                f"Total Records: {statistics['total']}",
                "",
                f"Resolved:      {statistics['resolved']:>5} ({statistics['resolution_rate']:.1f}%)",
                f"Review:        {statistics['review']:>5} ({statistics['review_rate']:.1f}%)",
                f"Unresolved:    {statistics['unresolved']:>5} ({statistics['unresolved_rate']:.1f}%)",
                "",
                f"Average Confidence: {statistics['average_confidence']:.2f}",
            ]
        )