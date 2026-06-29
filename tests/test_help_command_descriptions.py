from app.application import OpenFileService
from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands


def test_help_command_shows_descriptions():
    registry = CommandRegistry()

    register_default_commands(registry, OpenFileService())

    help_command = registry.get("help")

    assert help_command.execute() == (
        "General\n"
        "-------\n"
        "hello\n"
        "help\n"
        "\n"
        "File\n"
        "----\n"
        "open\n"
        "\n"
        "System\n"
        "------\n"
        "exit"
    )