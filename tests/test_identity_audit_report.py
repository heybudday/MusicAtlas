from app.services.identity_audit_report import IdentityAuditReport


def test_build_summary():
    report = IdentityAuditReport()

    results = [
        {
            "entity_type": "artist",
            "provider": "discogs",
            "status": "matched",
        },
        {
            "entity_type": "artist",
            "provider": "discogs",
            "status": "review",
        },
        {
            "entity_type": "label",
            "provider": "musicbrainz",
            "status": "matched",
        },
        {
            "entity_type": "label",
            "provider": "musicbrainz",
            "status": "unmatched",
        },
    ]

    summary = report.build(results)

    assert summary["artists"] == 2
    assert summary["labels"] == 2

    assert summary["matched"] == 2
    assert summary["review"] == 1
    assert summary["unmatched"] == 1

    assert summary["providers"]["discogs"]["matched"] == 1
    assert summary["providers"]["discogs"]["review"] == 1

    assert summary["providers"]["musicbrainz"]["matched"] == 1
    assert summary["providers"]["musicbrainz"]["unmatched"] == 1

    assert summary["success_rate"] == 50.0


def test_empty_summary():
    report = IdentityAuditReport()

    summary = report.build([])

    assert summary["artists"] == 0
    assert summary["labels"] == 0
    assert summary["matched"] == 0
    assert summary["review"] == 0
    assert summary["unmatched"] == 0
    assert summary["providers"] == {}
    assert summary["success_rate"] == 0.0


def test_format_report():
    report = IdentityAuditReport()

    summary = report.build(
        [
            {
                "entity_type": "artist",
                "provider": "discogs",
                "status": "matched",
            }
        ]
    )

    output = report.format(summary)

    assert "Music Atlas Identity Audit Report" in output
    assert "Artists scanned: 1" in output
    assert "Matched: 1" in output
    assert "Discogs" in output
    assert "Overall success rate: 100.0%" in output