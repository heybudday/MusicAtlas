from app.ui.exit_command import ExitCommand


def test_exit_command_returns_false():
    command = ExitCommand()

    assert command.execute() is False