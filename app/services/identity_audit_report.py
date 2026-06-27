from __future__ import annotations


class IdentityAuditReport:
    """
    Aggregates identity audit results into summary statistics.
    """

    def build(self, results):
        summary = {
            "artists": 0,
            "labels": 0,
            "matched": 0,
            "review": 0,
            "unmatched": 0,
            "providers": {},
            "success_rate": 0.0,
        }

        total_entities = len(results)

        if total_entities == 0:
            return summary

        for result in results:
            entity_type = result.get("entity_type")

            if entity_type == "artist":
                summary["artists"] += 1
            elif entity_type == "label":
                summary["labels"] += 1

            status = result.get("status")

            if status == "matched":
                summary["matched"] += 1
            elif status == "review":
                summary["review"] += 1
            elif status == "unmatched":
                summary["unmatched"] += 1

            provider = result.get("provider")

            if provider:
                provider_summary = summary["providers"].setdefault(
                    provider,
                    {
                        "matched": 0,
                        "review": 0,
                        "unmatched": 0,
                        "total": 0,
                    },
                )

                provider_summary["total"] += 1

                if status in provider_summary:
                    provider_summary[status] += 1

        summary["success_rate"] = round(
            (summary["matched"] / total_entities) * 100,
            2,
        )

        return summary

    def format(self, summary):
        lines = [
            "=" * 36,
            "Music Atlas Identity Audit Report",
            "=" * 36,
            "",
            f"Artists scanned: {summary['artists']}",
            f"Labels scanned: {summary['labels']}",
            "",
            f"Matched: {summary['matched']}",
            f"Needs review: {summary['review']}",
            f"Unmatched: {summary['unmatched']}",
            "",
        ]

        for provider in sorted(summary["providers"]):
            stats = summary["providers"][provider]

            lines.extend(
                [
                    provider.title(),
                    "-" * len(provider),
                    f"Matches: {stats['matched']}",
                    f"Reviews: {stats['review']}",
                    f"Unmatched: {stats['unmatched']}",
                    "",
                ]
            )

        lines.append(
            f"Overall success rate: {summary['success_rate']}%"
        )

        return "\n".join(lines)