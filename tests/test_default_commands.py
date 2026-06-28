from app.ui.command import Command
from app.ui.default_commands import register_default_commands
from app.ui.command_registry import CommandRegistry


def test_register_default_commands():
    registry = CommandRegistry()

    register_default_commands(registry)

    command = registry.get("hello")

    assert isinstance(command, Command)
    assert command.execute() == "hello"