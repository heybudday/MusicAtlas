from __future__ import annotations


class IdentityAudit:
    """
    Builds a machine-readable audit trail describing how
    identity resolution decisions were made.
    """

    def build(self, scored_result):
        result = scored_result.get("result", {})

        return {
            "provider": scored_result.get("provider"),
            "matched": result.get("matched", False),
            "confidence": scored_result.get("confidence", 0.0),
            "reason": scored_result.get("reason"),
            "evidence": result.get("evidence", []),
            "aliases_used": result.get("related_names", []),
            "selected": scored_result.get("selected", False),
            "persisted": scored_result.get("persisted", False),
            "review_required": scored_result.get(
                "review_required",
                False,
            ),
        }