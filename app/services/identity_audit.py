from __future__ import annotations


class IdentityAudit:
    """
    Runs identity audits for stored Music Atlas entities.
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def audit_artist(self, name: str) -> dict:
        result = self.orchestrator.enrich_artist(name)

        return {
            "entity_type": "artist",
            "query": name,
            "matched": result.get("matched", False),
            "provider": result.get("provider"),
            "confidence": result.get("confidence", 0.0),
            "reason": result.get("reason"),
            "review_recommended": result.get("review_recommended", False),
            "result": result.get("result"),
        }