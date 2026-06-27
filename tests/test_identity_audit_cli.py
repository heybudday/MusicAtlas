from unittest.mock import MagicMock, patch

from app.cli.identity_audit import main


@patch("sys.argv", ["identity_audit"])
@patch("app.cli.identity_audit.SessionLocal")
@patch("app.cli.identity_audit.IdentityAuditRunner")
def test_identity_audit_cli(mock_runner_class, mock_session_local, capsys):
    session = MagicMock()
    mock_session_local.return_value = session

    runner = MagicMock()
    runner.run_all.return_value = {
        "processed": 10,
        "success": 8,
        "review": 1,
        "failed": 1,
    }
    mock_runner_class.return_value = runner

    main()

    mock_session_local.assert_called_once()
    mock_runner_class.assert_called_once_with(session)
    runner.run_all.assert_called_once()
    session.close.assert_called_once()

    output = capsys.readouterr().out

    assert "Music Atlas Identity Audit" in output
    assert "Processed:   10" in output
    assert "Successful: 8" in output
    assert "Review:     1" in output
    assert "Failed:     1" in output
    assert "Done." in output


@patch("sys.argv", ["identity_audit", "dashboard"])
@patch("app.cli.identity_audit.SessionLocal")
@patch("app.cli.identity_audit.IdentityAuditRunner")
def test_identity_audit_dashboard_cli(
    mock_runner_class,
    mock_session_local,
    capsys,
):
    session = MagicMock()
    mock_session_local.return_value = session

    runner = MagicMock()
    runner.run_all.return_value = {
        "summary": {
            "processed": 3,
            "success": 1,
            "review": 1,
            "failed": 1,
        },
        "results": [
            {
                "matched": True,
                "review_recommended": False,
                "confidence": 0.95,
                "provider": "discogs",
                "issues": [],
                "audited_at": "2026-06-27 15:30:00",
            },
            {
                "matched": True,
                "review_recommended": True,
                "confidence": 0.82,
                "provider": "musicbrainz",
                "issues": ["ambiguous_identity"],
                "audited_at": "2026-06-27 15:45:00",
            },
            {
                "matched": False,
                "review_recommended": False,
                "confidence": 0.0,
                "provider": "discogs",
                "issues": ["missing_spotify"],
                "audited_at": "2026-06-27 15:15:00",
            },
        ],
    }
    mock_runner_class.return_value = runner

    main()

    mock_session_local.assert_called_once()
    mock_runner_class.assert_called_once_with(session)
    runner.run_all.assert_called_once()
    session.close.assert_called_once()

    output = capsys.readouterr().out

    assert "Identity Audit Dashboard" in output
    assert "Artists audited: 3" in output
    assert "Passed:         1" in output
    assert "Needs Review:   1" in output
    assert "Failed:         1" in output
    assert "High:           1" in output
    assert "Medium:         1" in output
    assert "Low:            1" in output
    assert "discogs: 2" in output
    assert "musicbrainz: 1" in output
    assert "ambiguous_identity: 1" in output
    assert "missing_spotify: 1" in output
    assert "Last Audit: 2026-06-27 15:45:00" in output