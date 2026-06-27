from __future__ import annotations


class AutomaticIdentityResolution:
    AUTO_APPROVE = "AUTO_APPROVE"
    REVIEW = "REVIEW"
    REJECT = "REJECT"

    AUDIT_AUTO_APPROVED = "AUTO_APPROVED"
    AUDIT_REVIEW_REQUIRED = "REVIEW_REQUIRED"
    AUDIT_AUTO_REJECTED = "AUTO_REJECTED"

    def __init__(
        self,
        orchestrator,
        decision_service,
        external_identity_service=None,
        audit_history=None,
        review_queue=None,
    ):
        self.orchestrator = orchestrator
        self.decision_service = decision_service
        self.external_identity_service = external_identity_service
        self.audit_history = audit_history
        self.review_queue = review_queue

    def resolve(self, query):
        candidate = self.orchestrator.resolve(query)
        decision = self.decision_service.decide(candidate)

        result = {
            "decision": decision,
            "confidence": candidate.get("confidence"),
            "provider": candidate.get("provider"),
            "result": candidate.get("result"),
        }

        if decision == self.AUTO_APPROVE:
            self._persist_identity(query, candidate)
            self._record_audit(query, candidate, self.AUDIT_AUTO_APPROVED)
        elif decision == self.REVIEW:
            self._queue_for_review(query, candidate)
            self._record_audit(query, candidate, self.AUDIT_REVIEW_REQUIRED)
        else:
            self._record_audit(query, candidate, self.AUDIT_AUTO_REJECTED)

        return result

    def _persist_identity(self, query, candidate):
        if self.external_identity_service is None:
            return

        self.external_identity_service.upsert_identity(
            artist_name=query,
            provider=candidate.get("provider"),
            external_id=candidate.get("result", {}).get("external_id"),
            url=candidate.get("result", {}).get("url"),
            confidence=candidate.get("confidence"),
            raw_data=candidate.get("result"),
        )

    def _queue_for_review(self, query, candidate):
        if self.review_queue is None:
            return

        self.review_queue.add(
            artist_name=query,
            provider=candidate.get("provider"),
            confidence=candidate.get("confidence"),
            result=candidate.get("result"),
        )

    def _record_audit(self, query, candidate, action):
        if self.audit_history is None:
            return

        self.audit_history.record(
            artist_name=query,
            provider=candidate.get("provider"),
            confidence=candidate.get("confidence"),
            action=action,
            result=candidate.get("result"),
        )
