from app.services.automatic_identity_resolution import AutomaticIdentityResolution


class FakeOrchestrator:
    def __init__(self, candidate):
        self.candidate = candidate

    def resolve(self, query):
        return self.candidate


class FakeDecisionService:
    def __init__(self, decision):
        self.decision = decision

    def decide(self, candidate):
        return self.decision


class FakeExternalIdentityService:
    def __init__(self):
        self.persisted = []

    def upsert_identity(self, **kwargs):
        self.persisted.append(kwargs)


class FakeAuditHistory:
    def __init__(self):
        self.records = []

    def record(self, **kwargs):
        self.records.append(kwargs)


class FakeReviewQueue:
    def __init__(self):
        self.items = []

    def add(self, **kwargs):
        self.items.append(kwargs)


def make_candidate(confidence=0.97):
    return {
        "provider": "discogs",
        "confidence": confidence,
        "result": {
            "external_id": "123",
            "name": "Daft Punk",
            "url": "https://www.discogs.com/artist/123-Daft-Punk",
        },
    }


def test_auto_approve_persists_identity_and_records_audit():
    external_identity_service = FakeExternalIdentityService()
    audit_history = FakeAuditHistory()
    review_queue = FakeReviewQueue()

    service = AutomaticIdentityResolution(
        orchestrator=FakeOrchestrator(make_candidate(confidence=0.97)),
        decision_service=FakeDecisionService("AUTO_APPROVE"),
        external_identity_service=external_identity_service,
        audit_history=audit_history,
        review_queue=review_queue,
    )

    result = service.resolve("Daft Punk")

    assert result["decision"] == "AUTO_APPROVE"
    assert result["confidence"] == 0.97
    assert result["provider"] == "discogs"
    assert result["result"]["external_id"] == "123"

    assert len(external_identity_service.persisted) == 1
    assert external_identity_service.persisted[0]["artist_name"] == "Daft Punk"
    assert external_identity_service.persisted[0]["provider"] == "discogs"
    assert external_identity_service.persisted[0]["external_id"] == "123"

    assert review_queue.items == []

    assert len(audit_history.records) == 1
    assert audit_history.records[0]["action"] == "AUTO_APPROVED"


def test_review_required_queues_candidate_and_records_audit():
    external_identity_service = FakeExternalIdentityService()
    audit_history = FakeAuditHistory()
    review_queue = FakeReviewQueue()

    service = AutomaticIdentityResolution(
        orchestrator=FakeOrchestrator(make_candidate(confidence=0.84)),
        decision_service=FakeDecisionService("REVIEW"),
        external_identity_service=external_identity_service,
        audit_history=audit_history,
        review_queue=review_queue,
    )

    result = service.resolve("Daft Punk")

    assert result["decision"] == "REVIEW"
    assert result["confidence"] == 0.84
    assert result["provider"] == "discogs"

    assert external_identity_service.persisted == []

    assert len(review_queue.items) == 1
    assert review_queue.items[0]["artist_name"] == "Daft Punk"
    assert review_queue.items[0]["provider"] == "discogs"
    assert review_queue.items[0]["confidence"] == 0.84

    assert len(audit_history.records) == 1
    assert audit_history.records[0]["action"] == "REVIEW_REQUIRED"


def test_reject_records_audit_without_persisting_or_queueing():
    external_identity_service = FakeExternalIdentityService()
    audit_history = FakeAuditHistory()
    review_queue = FakeReviewQueue()

    service = AutomaticIdentityResolution(
        orchestrator=FakeOrchestrator(make_candidate(confidence=0.0)),
        decision_service=FakeDecisionService("REJECT"),
        external_identity_service=external_identity_service,
        audit_history=audit_history,
        review_queue=review_queue,
    )

    result = service.resolve("Unknown Artist")

    assert result["decision"] == "REJECT"
    assert result["confidence"] == 0.0
    assert result["provider"] == "discogs"

    assert external_identity_service.persisted == []
    assert review_queue.items == []

    assert len(audit_history.records) == 1
    assert audit_history.records[0]["action"] == "AUTO_REJECTED"


def test_returned_result_includes_decision_confidence_provider_and_result():
    candidate = make_candidate(confidence=0.95)

    service = AutomaticIdentityResolution(
        orchestrator=FakeOrchestrator(candidate),
        decision_service=FakeDecisionService("AUTO_APPROVE"),
    )

    result = service.resolve("Daft Punk")

    assert result == {
        "decision": "AUTO_APPROVE",
        "confidence": 0.95,
        "provider": "discogs",
        "result": candidate["result"],
    }