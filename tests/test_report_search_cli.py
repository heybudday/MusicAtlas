from __future__ import annotations

import json
from pathlib import Path

from app.cli.report_search import main


def write_report(path: Path, filename: str, data: dict) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / filename).write_text(json.dumps(data), encoding="utf-8")


def test_search_cli_prints_matching_reports(tmp_path, capsys):
    archive_dir = tmp_path / "reports"

    write_report(
        archive_dir,
        "jeff-mills.json",
        {
            "report_type": "identity",
            "artist": "Jeff Mills",
        },
    )
    write_report(
        archive_dir,
        "robert-hood.json",
        {
            "report_type": "identity",
            "artist": "Robert Hood",
        },
    )

    exit_code = main(["Jeff", "--archive-dir", str(archive_dir)])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "jeff-mills.json" in output
    assert "Jeff Mills" in output
    assert "robert-hood.json" not in output


def test_search_cli_filters_by_report_type(tmp_path, capsys):
    archive_dir = tmp_path / "reports"

    write_report(
        archive_dir,
        "identity.json",
        {
            "report_type": "identity",
            "artist": "Jeff Mills",
        },
    )
    write_report(
        archive_dir,
        "audit.json",
        {
            "report_type": "audit",
            "artist": "Jeff Mills",
        },
    )

    exit_code = main(
        [
            "Jeff",
            "--archive-dir",
            str(archive_dir),
            "--report-type",
            "identity",
        ]
    )

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "identity.json" in output
    assert "audit.json" not in output


def test_search_cli_returns_all_when_no_filters(tmp_path, capsys):
    archive_dir = tmp_path / "reports"

    write_report(
        archive_dir,
        "identity.json",
        {
            "report_type": "identity",
            "artist": "Jeff Mills",
        },
    )
    write_report(
        archive_dir,
        "audit.json",
        {
            "report_type": "audit",
            "artist": "Robert Hood",
        },
    )

    exit_code = main(["--archive-dir", str(archive_dir)])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "identity.json" in output
    assert "audit.json" in output


def test_search_cli_prints_message_when_no_results(tmp_path, capsys):
    archive_dir = tmp_path / "reports"

    write_report(
        archive_dir,
        "jeff-mills.json",
        {
            "report_type": "identity",
            "artist": "Jeff Mills",
        },
    )

    exit_code = main(["Aphex", "--archive-dir", str(archive_dir)])

    output = capsys.readouterr().out

    assert exit_code == 0
    assert "No matching reports found." in output