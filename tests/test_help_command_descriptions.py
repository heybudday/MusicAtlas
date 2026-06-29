from app.application import OpenFileService
from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands


def test_help_command_shows_descriptions():
    registry = CommandRegistry()

    register_default_commands(registry, OpenFileService())

    help_command = registry.get("help")

    assert help_command.execute() == (
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