from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.cli.identity_audit import main


@patch(
    "sys.argv",
    [
        "identity_audit",
        "--format",
        "json",
        "--output-dir",
        "reports-test",
    ],
)
@patch("app.cli.identity_audit.IdentityAuditExporter")
@patch("app.cli.identity_audit.SessionLocal")
@patch("app.cli.identity_audit.IdentityAuditRunner")
def test_identity_audit_cli_exports_json(
    mock_runner_class,
    mock_session_local,
    mock_exporter_class,
    capsys,
):
    session = MagicMock()
    mock_session_local.return_value = session

    runner = MagicMock()
    runner.run_all.return_value = {
        "summary": {
            "processed": 2,
            "success": 1,
            "review": 1,
            "failed": 0,
        },
        "results": [
            {
                "query": "Aphex Twin",
                "status": "matched",
            },
            {
                "query": "Unknown Artist",
                "status": "review",
            },
        ],
    }
    mock_runner_class.return_value = runner

    exporter = MagicMock()
    exporter.export.return_value = ["reports-test/identity_audit_test.json"]
    mock_exporter_class.return_value = exporter

    main()

    mock_exporter_class.assert_called_once_with("reports-test")
    exporter.export.assert_called_once_with(
        summary={
            "processed": 2,
            "success": 1,
            "review": 1,
            "failed": 0,
        },
        results=[
            {
                "query": "Aphex Twin",
                "status": "matched",
            },
            {
                "query": "Unknown Artist",
                "status": "review",
            },
        ],
        export_format="json",
    )

    output = capsys.readouterr().out

    assert "Exported:" in output
    assert "reports-test/identity_audit_test.json" in output
    assert "Done." in output


@patch(
    "sys.argv",
    [
        "identity_audit",
        "--format",
        "both",
    ],
)
@patch("app.cli.identity_audit.IdentityAuditExporter")
@patch("app.cli.identity_audit.SessionLocal")
@patch("app.cli.identity_audit.IdentityAuditRunner")
def test_identity_audit_cli_exports_both_with_default_output_dir(
    mock_runner_class,
    mock_session_local,
    mock_exporter_class,
):
    session = MagicMock()
    mock_session_local.return_value = session

    runner = MagicMock()
    runner.run_all.return_value = {
        "processed": 1,
        "success": 1,
        "review": 0,
        "failed": 0,
    }
    mock_runner_class.return_value = runner

    exporter = MagicMock()
    exporter.export.return_value = [
        "reports/identity_audit_test.json",
        "reports/identity_audit_test.csv",
    ]
    mock_exporter_class.return_value = exporter

    main()

    mock_exporter_class.assert_called_once_with("reports")
    exporter.export.assert_called_once_with(
        summary={
            "processed": 1,
            "success": 1,
            "review": 0,
            "failed": 0,
        },
        results=[],
        export_format="both",
    )