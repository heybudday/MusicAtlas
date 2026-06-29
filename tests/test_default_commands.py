from app.application import OpenFileService
from app.ui.command import Command
from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands


def test_register_default_commands():
    registry = CommandRegistry()

    register_default_commands(registry, OpenFileService())

    command = registry.get("hello")

    assert isinstance(command, Command)
    assert command.execute() == "hello"