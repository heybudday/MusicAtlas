from app.application import Application


def test_help_groups_commands_by_category():
    app = Application.create()

    result = app.shell.run_once("help")

    assert result == (
        "File\n"
        "----\n"
        "open - Opens a file\n"
        "Usage: open <filename>\n"
        "\n"
        "General\n"
        "-------\n"
        "hello - Say hello\n"
        "Usage: hello\n"
        "help - Show available commands\n"
        "Usage: help\n"
        "\n"
        "System\n"
        "------\n"
        "exit - Exit the application\n"
        "Usage: exit"
    )