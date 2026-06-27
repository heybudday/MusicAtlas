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