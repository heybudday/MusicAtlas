from app.application import Application


def test_help_command_displays_usage():
    app = Application.create()

    result = app.shell.run_once("help")

    assert "hello" in result
    assert "Usage: hello" in result

    assert "help" in result
    assert "Usage: help" in result

    assert "open" in result
    assert "Usage: open <filename>" in result

    assert "exit" in result
    assert "Usage: exit" in result