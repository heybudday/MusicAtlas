from app.ui.command_registry import CommandRegistry
from app.ui.default_commands import register_default_commands


def test_registry_can_enumerate_commands():
    registry = CommandRegistry()

    register_default_commands(registry)

    commands = registry.list_commands()

    assert [command.name for command in commands] == ["hello", "help", "exit"]