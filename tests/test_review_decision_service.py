from app.services.review_decision_service import ReviewDecisionService


class FakeRepository:
    def __init__(self):
        self.persisted = []

    def persist(self, item):
        self.persisted.append(dict(item))


class FakeAuditHistory:
    def __init__(self):
        self.entries = []

    def record(self, item, action):
        self.entries.append(
            {
                "status": item["status"],
                "action": action,
            }
        )


def make_item():
    return {
        "artist": "Orbital",
        "status": "pending",
    }


def test_approve_updates_status():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    result = service.approve(item)

    assert result["status"] == "approved"


def test_approve_persists_enrichment():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    service.approve(item)

    assert len(repo.persisted) == 1
    assert repo.persisted[0]["status"] == "approved"


def test_approve_records_history():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    service.approve(item)

    assert len(audit.entries) == 1
    assert audit.entries[0]["action"] == "approved"


def test_reject_updates_status():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    service.reject(item)

    assert item["status"] == "rejected"


def test_reject_does_not_persist():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    service.reject(item)

    assert repo.persisted == []


def test_reject_records_history():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    service.reject(item)

    assert len(audit.entries) == 1
    assert audit.entries[0]["action"] == "rejected"


def test_skip_leaves_pending():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    service.skip(item)

    assert item["status"] == "pending"
    assert repo.persisted == []
    assert audit.entries == []


def test_process_approve():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    result = service.process(item, "approve")

    assert result["status"] == "approved"


def test_process_reject():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    result = service.process(item, "reject")

    assert result["status"] == "rejected"


def test_process_skip():
    repo = FakeRepository()
    audit = FakeAuditHistory()

    service = ReviewDecisionService(repo, audit)

    item = make_item()

    result = service.process(item, "skip")

    assert result["status"] == "pending"


def test_invalid_decision_raises():
    service = ReviewDecisionService()

    item = make_item()

    try:
        service.process(item, "banana")
        assert False
    except ValueError:
        assert True