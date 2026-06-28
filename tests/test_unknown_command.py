from app.application import Application


def test_unknown_command_returns_message():
    app = Application.create()

    result = app.shell.run_once("doesnotexist")

    assert result == "Unknown command: doesnotexist"