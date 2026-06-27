from app.services.identity_audit_history import IdentityAuditHistory


def test_identical_reports():
    history = IdentityAuditHistory()

    report = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "confidence": 1.0,
            "provider": "discogs",
            "review_recommended": False,
        }
    ]

    result = history.compare(report, report)

    for value in result.values():
        assert value == []


def test_new_match():
    history = IdentityAuditHistory()

    previous = []

    current = [
        {
            "entity_type": "artist",
            "query": "Orbital",
        }
    ]

    result = history.compare(previous, current)

    assert len(result["new_matches"]) == 1


def test_lost_match():
    history = IdentityAuditHistory()

    previous = [
        {
            "entity_type": "artist",
            "query": "Orbital",
        }
    ]

    current = []

    result = history.compare(previous, current)

    assert len(result["lost_matches"]) == 1


def test_confidence_increase():
    history = IdentityAuditHistory()

    previous = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "confidence": 0.55,
        }
    ]

    current = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "confidence": 0.95,
        }
    ]

    result = history.compare(previous, current)

    assert len(result["confidence_increased"]) == 1


def test_confidence_decrease():
    history = IdentityAuditHistory()

    previous = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "confidence": 0.95,
        }
    ]

    current = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "confidence": 0.60,
        }
    ]

    result = history.compare(previous, current)

    assert len(result["confidence_decreased"]) == 1


def test_new_review_candidate():
    history = IdentityAuditHistory()

    previous = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "review_recommended": False,
        }
    ]

    current = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "review_recommended": True,
        }
    ]

    result = history.compare(previous, current)

    assert len(result["new_review_candidates"]) == 1


def test_resolved_review():
    history = IdentityAuditHistory()

    previous = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "review_recommended": True,
        }
    ]

    current = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "review_recommended": False,
        }
    ]

    result = history.compare(previous, current)

    assert len(result["resolved_reviews"]) == 1


def test_provider_change():
    history = IdentityAuditHistory()

    previous = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "provider": "discogs",
        }
    ]

    current = [
        {
            "entity_type": "artist",
            "query": "Orbital",
            "provider": "musicbrainz",
        }
    ]

    result = history.compare(previous, current)

    assert len(result["provider_changes"]) == 1


def test_empty_reports():
    history = IdentityAuditHistory()

    result = history.compare([], [])

    for value in result.values():
        assert value == []


def test_missing_fields_are_handled():
    history = IdentityAuditHistory()

    previous = [
        {
            "entity_type": "artist",
            "query": "Orbital",
        }
    ]

    current = [
        {
            "entity_type": "artist",
            "query": "Orbital",
        }
    ]

    result = history.compare(previous, current)

    for value in result.values():
        assert value == []