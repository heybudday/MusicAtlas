from __future__ import annotations


class IdentityAuditHistory:
    """
    Compares two identity audit reports and summarizes the changes.
    """

    def compare(self, previous_report, current_report):
        previous = {self._key(item): item for item in (previous_report or [])}
        current = {self._key(item): item for item in (current_report or [])}

        results = {
            "new_matches": [],
            "lost_matches": [],
            "confidence_increased": [],
            "confidence_decreased": [],
            "new_review_candidates": [],
            "resolved_reviews": [],
            "provider_changes": [],
        }

        previous_keys = set(previous)
        current_keys = set(current)

        for key in sorted(current_keys - previous_keys):
            results["new_matches"].append(current[key])

        for key in sorted(previous_keys - current_keys):
            results["lost_matches"].append(previous[key])

        for key in sorted(previous_keys & current_keys):
            old = previous[key]
            new = current[key]

            old_confidence = old.get("confidence", 0.0) or 0.0
            new_confidence = new.get("confidence", 0.0) or 0.0

            if new_confidence > old_confidence:
                results["confidence_increased"].append(
                    {
                        "previous": old,
                        "current": new,
                    }
                )

            elif new_confidence < old_confidence:
                results["confidence_decreased"].append(
                    {
                        "previous": old,
                        "current": new,
                    }
                )

            old_review = bool(old.get("review_recommended"))
            new_review = bool(new.get("review_recommended"))

            if not old_review and new_review:
                results["new_review_candidates"].append(
                    {
                        "previous": old,
                        "current": new,
                    }
                )

            elif old_review and not new_review:
                results["resolved_reviews"].append(
                    {
                        "previous": old,
                        "current": new,
                    }
                )

            if old.get("provider") != new.get("provider"):
                results["provider_changes"].append(
                    {
                        "previous": old,
                        "current": new,
                    }
                )

        return results

    def _key(self, item):
        return (
            item.get("entity_type"),
            item.get("query"),
        )
