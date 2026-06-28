from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands


def test_help_command_lists_registered_commands():
    registry = CommandRegistry()

    register_default_commands(registry)

    command = registry.get("help")

    assert command.execute() == "hello\nhelp"