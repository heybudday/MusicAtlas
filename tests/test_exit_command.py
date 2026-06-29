from app.application import OpenFileService
from app.ui.command import Command
from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands


def test_exit_command_is_registered():
    registry = CommandRegistry()

    register_default_commands(registry, OpenFileService())

    command = registry.get("exit")

    assert isinstance(command, Command)